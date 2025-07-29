from langgraph.graph import StateGraph, END
from config import AgentState, AgentConfig
from llm_manager import llm_manager
import memos_manager
import progenitor # CORRECT: Import the standalone progenitor module
import json

class JaraxxusGraph:
    """
    This class defines the core orchestration logic for the Jaraxxus agent using LangGraph.
    """
    def __init__(self, memos: memos_manager.MemOSManager):
        self.memos = memos
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """
        Constructs the complete state graph with all nodes and conditional edges.
        """
        workflow = StateGraph(AgentState)

        # Node Definitions
        workflow.add_node("plan", self.plan_step)
        workflow.add_node("execute", self.execute_step)
        workflow.add_node("reflect", self.reflect_step)
        workflow.add_node("human_in_the_loop", self.human_in_the_loop_step)
        workflow.add_node("progenitor", self.progenitor_step)
        workflow.add_node("learn", self.learn_step)

        # Edge Definitions
        workflow.set_entry_point("plan")
        workflow.add_edge("plan", "execute")
        workflow.add_edge("progenitor", "execute")
        workflow.add_edge("learn", END)

        workflow.add_conditional_edges("execute", self.should_continue)
        workflow.add_conditional_edges("reflect", self.after_reflection)
        workflow.add_conditional_edges("human_in_the_loop", self.after_hitl)

        return workflow.compile()

    # --- Node Implementations ---

    def plan_step(self, state: AgentState) -> AgentState:
        print("\n---PLANNING---")
        prompt = f"Task: {state['task']}"
        system_prompt = """You are the Orchestrator... Create a structured plan...""" # Abridged
        response = llm_manager.run_orchestrator(prompt, system_prompt)
        state["plan"] = response.get("plan", [])
        state["trace"].append({"state": "planned", "plan": state["plan"]})
        self.memos.update_scratchpad({"current_plan": state["plan"]})
        return state

    def execute_step(self, state: AgentState) -> AgentState:
        print("\n---EXECUTING---")
        if not state.get("plan"):
            state["error_message"] = "Execution cannot proceed without a plan."
            state["error"] = True
            return state

        step_details = state["plan"][0]
        step = step_details.get("step", "No step defined.")
        specialist = step_details.get("specialist", "code_specialist")
        print(f"Task: '{step}' with '{specialist}'")

        model = AgentConfig.CODE_SPECIALIST_MODEL if specialist == "code_specialist" else AgentConfig.FILE_IO_SPECIALIST_MODEL
        result_dict = llm_manager.run_specialist_with_tools(model, step)

        tool_output = result_dict.get("output", "")
        if "error" in result_dict or "Error" in str(tool_output):
            outcome = "FAILURE"
            state["error"] = True
            state["error_message"] = str(tool_output) or result_dict.get("error")
        else:
            outcome = "SUCCESS"
            state["error"] = False

        action_log = {
            "step": step,
            "specialist": specialist,
            "tool_call": result_dict.get("tool", "none"),
            "tool_input": result_dict.get("input", "none"),
            "result": tool_output,
            "outcome": outcome
        }

        state["plan"] = state["plan"][1:]
        state["trace"].append({"state": "executed", "action": action_log})
        state["failed_action"] = action_log if outcome == "FAILURE" else {}
        self.memos.update_scratchpad(state)
        return state

    def reflect_step(self, state: AgentState) -> AgentState:
        print("\n---REFLECTING ON FAILURE---")
        failed_action = state.get("failed_action", {})
        system_prompt = "You are an expert debugging agent..."
        prompt = f"Original Task: {state['task']}\nFailed Step: {failed_action.get('step')}\nError Log: {state['error_message']}"
        response = llm_manager.run_orchestrator(prompt, system_prompt)
        root_cause = response.get('root_cause', 'Unknown failure cause')
        state['progenitor_query'] = root_cause

        past_solutions = self.memos.search_codex(root_cause)
        if not past_solutions:
            print("No past solutions found in Codex. Proceeding to HITL.")
            state["is_novel_error"] = True
        else:
            print(f"Found {len(past_solutions)} solution(s) in Codex.")
            state["is_novel_error"] = False
            system_prompt = "You are the Orchestrator. A previous plan failed... Formulate a revised plan..."
            prompt = f"Original Task: {state['task']}\nRoot Cause: {root_cause}\nGuidance from Codex: {json.dumps(past_solutions)}"
            new_plan_response = llm_manager.run_orchestrator(prompt, system_prompt)
            state["plan"] = new_plan_response.get("plan", [])
            state["error"] = False
        return state

    def human_in_the_loop_step(self, state: AgentState) -> AgentState:
        print("\n" + "!"*50 + "\nNOVEL ERROR DETECTED - HUMAN ASSISTANCE REQUIRED\n" + "!"*50)
        print(f"Problem Analysis: {state['progenitor_query']}")
        user_input = input(
            "1. Attempt to formulate a new plan and learn from it.\n"
            "2. Escalate to Gemini Progenitor for strategy.\n"
            "3. Provide a direct plan (e.g., 'step one;step two'):\n> "
        )
        state["human_feedback"] = user_input
        state["error"] = False
        return state

    def progenitor_step(self, state: AgentState) -> AgentState:
        print("\n---ESCALATING TO PROGENITOR---")
        # CORRECT: This now calls the standalone progenitor module.
        strategy = progenitor.analyze_unsolvable_error([state["error_message"]])
        
        print(f"---PROGENITOR'S STRATEGIC ADVICE---\n{strategy}")
        
        system_prompt = "You are the Orchestrator... Turn this advice into a concrete, structured plan."
        prompt = f"Original Task: {state['task']}\nRoot Cause: {state['progenitor_query']}\nProgenitor Advice: {strategy}"
        new_plan_response = llm_manager.run_orchestrator(prompt, system_prompt)
        
        state["plan"] = new_plan_response.get("plan", [])
        state["error"] = False
        state["human_feedback"] = f"Progenitor intervention: {strategy}"
        return state

    def learn_step(self, state: AgentState) -> AgentState:
        print("\n---LEARNING FROM EXPERIENCE---")
        failure_index = next((i for i, event in enumerate(state["trace"]) if event.get("action", {}).get("outcome") == "FAILURE"), -1)
        if failure_index != -1:
            failure_pattern = [e['action'] for e in state["trace"][:failure_index+1] if 'action' in e]
            successful_resolution = [e['action'] for e in state["trace"][failure_index+1:] if 'action' in e]
            self.memos.add_lesson_to_codex(
                problem_signature=state['progenitor_query'],
                failure_pattern=failure_pattern,
                successful_resolution=successful_resolution,
                human_guidance=state['human_feedback']
            )
        state["is_novel_error"] = False
        return state

    # --- Conditional Edges ---
    def should_continue(self, state: AgentState):
        if state["error"]:
            return "reflect"
        if not state.get("plan"):
            return "learn" if state.get("is_novel_error") else END
        return "execute"

    def after_reflection(self, state: AgentState):
        return "human_in_the_loop" if state.get("is_novel_error") else "execute"

    def after_hitl(self, state: AgentState):
        if state["human_feedback"] == "2":
            return "progenitor"
        
        guidance = ""
        if state["human_feedback"].startswith("3:"):
            plan_str = state["human_feedback"].split(":", 1)[1]
            guidance = f"User provided the following direct plan: {plan_str}"
        else:
            guidance = "User authorized a novel first-attempt plan."
            
        system_prompt = "You are the Orchestrator. Create a new plan based on the user's guidance."
        prompt = f"Original Task: {state['task']}\nRoot Cause: {state['progenitor_query']}\nGuidance: {guidance}"
        new_plan_response = llm_manager.run_orchestrator(prompt, system_prompt)
        state["plan"] = new_plan_response.get("plan", [])
        return "execute"
