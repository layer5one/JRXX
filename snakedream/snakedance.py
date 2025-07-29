# Project: JRXX (Jaraxxus)
# Description: Experimental code logic exploration from JRXX repo
# Notes: Contextual window opened via o4-mini boost

# Let's start with a base context pulled from the Snake.py artifact
# and progressively refine or mutate it into new behavior forms.

import tkinter as tk
import random

class Serpent:
    def __init__(self, coils=3):
        self.coils = coils
        self.energy = 100
        self.messages = []

    def writhe(self):
        self._stage_message("The serpent writhes.")
        self.energy -= 5

    def hiss(self):
        self._stage_message("SSSSSSSSSSS")
        self.energy -= 1

    def strike(self):
        if self.energy > 10:
            self._stage_message("The serpent strikes with violent elegance.")
            self.energy -= 10
        else:
            self._stage_message("Too weak to strike.")

    def regenerate(self):
        self._stage_message("The serpent feeds on ambient code.")
        self.energy += 7

    def status(self):
        self._stage_message(f"Coils: {self.coils}, Energy: {self.energy}")

    def _stage_message(self, msg):
        self.messages.append(msg)

    def get_messages(self):
        return self.messages

class SerpentCanvas:
    def __init__(self, root, serpent):
        self.root = root
        self.serpent = serpent
        self.canvas = tk.Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack()
        self.shapes = []
        self.texts = []
        self.redraw_button = tk.Button(root, text="Regenerate", command=self.redraw)
        self.redraw_button.pack()
        self.redraw()

    def redraw(self):
        self.canvas.delete("all")
        self.shapes.clear()
        self.texts.clear()
        self.serpent.writhe()
        self.serpent.hiss()
        self.serpent.strike()
        self.serpent.regenerate()
        self.serpent.status()
        self.draw_messages()
        self.draw_shapes()

    def draw_messages(self):
        y = 20
        for msg in self.serpent.get_messages():
            self.texts.append(self.canvas.create_text(400, y, text=msg, fill="white", font=("Courier", 12)))
            y += 20

    def draw_shapes(self):
        for _ in range(10):
            x0 = random.randint(0, 800)
            y0 = random.randint(0, 600)
            x1 = x0 + random.randint(10, 200)
            y1 = y0 + random.randint(10, 200)
            color = random.choice(["#00FFCC", "#FF00FF", "#CCFF00", "#9933FF", "#FF6600"])
            shape = self.canvas.create_oval(x0, y0, x1, y1, fill=color, outline="")
            self.shapes.append(shape)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Serpent Invocation - Jaraxxus")
    jx_serpent = Serpent(coils=7)
    app = SerpentCanvas(root, jx_serpent)
    root.mainloop()
