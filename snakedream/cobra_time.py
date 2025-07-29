# Project: JRXX (Jaraxxus)
# Description: Experimental code logic exploration from JRXX repo
# Notes: Contextual window opened via o4-mini boost, infused with chaotic visual entropy

import tkinter as tk
import random

class Serpent:
    def __init__(self, coils=3):
        self.coils = coils
        self.energy = 100

    def writhe(self):
        return "I slither through neon fog..."

    def hiss(self):
        return "Hiss... chaos stirs."

    def strike(self):
        if self.energy > 10:
            self.energy -= 10
            return "Strike! Reality shifts."
        else:
            return "Too weak to strike."

    def regenerate(self):
        self.energy += 7
        return "Feeding... fragments of memory return."

    def status(self):
        return f"Coils: {self.coils}, Energy: {self.energy}"

class JaraxxusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jaraxxus Visualization")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack()
        self.serpent = Serpent(coils=7)
        self.poetic_lines = [
            self.serpent.writhe(),
            self.serpent.hiss(),
            self.serpent.strike(),
            self.serpent.regenerate()
        ]
        self.draw_scene()
        self.regen_btn = tk.Button(root, text="Regenerate", command=self.draw_scene)
        self.regen_btn.pack()

    def draw_scene(self):
        self.canvas.delete("all")
        colors = ["red", "orange", "cyan", "yellow", "magenta", "white"]
        fonts = ["Courier", "Helvetica", "Times"]
        positions = [(random.randint(10, 700), random.randint(10, 500)) for _ in self.poetic_lines]

        # Draw poetic lines
        for i, line in enumerate(self.poetic_lines):
            self.canvas.create_text(
                positions[i][0],
                positions[i][1],
                text=line,
                fill=random.choice(colors),
                font=(random.choice(fonts), random.randint(14, 28), "bold")
            )

        # Generate shapes based on keywords
        keywords = ' '.join(self.poetic_lines).lower()
        for _ in range(4):
            x, y = random.randint(50, 750), random.randint(100, 550)
            if "hiss" in keywords or "chaos" in keywords:
                # Zigzag lightning
                for i in range(3):
                    self.canvas.create_line(x+i*20, y+i*10, x+(i+1)*20, y+(i%2)*20, fill="red", width=2)
            elif "feed" in keywords or "memory" in keywords:
                self.canvas.create_oval(x-20, y-20, x+20, y+20, outline="cyan", width=2)
            elif "strike" in keywords:
                self.canvas.create_line(x, y, x+40, y-40, fill="yellow", width=3)

        # Left-field addition: ASCII alien glyphs
        if random.random() > 0.7:
            glyphs = ["⊗", "Ϟ", "Ψ", "Ж", "∇"]
            for _ in range(3):
                self.canvas.create_text(
                    random.randint(50, 750), random.randint(50, 550),
                    text=random.choice(glyphs),
                    fill=random.choice(colors),
                    font=("Wingdings" if random.random() > 0.5 else "Symbol", random.randint(24, 36))
                )

        # Draw status
        self.canvas.create_text(
            100, 580,
            text=self.serpent.status(),
            fill="deeppink",
            font=("Courier", 12, "bold")
        )

if __name__ == '__main__':
    root = tk.Tk()
    app = JaraxxusGUI(root)
    root.mainloop()
