# Project: JRXX (Jaraxxus)
# Description: Experimental code logic exploration from JRXX repo
# Notes: Contextual window opened via o4-mini boost

import tkinter as tk
import random

class Serpent:
    def __init__(self, coils=3):
        self.coils = coils
        self.energy = 100

    def writhe(self):
        return ("writhe", "I slither through neon fog...", "orange")

    def hiss(self):
        self.energy -= 1
        return ("hiss", "Hiss... chaos stirs.", "magenta")

    def strike(self):
        if self.energy > 10:
            self.energy -= 10
            return ("strike", "Strike! Reality shifts.", "white")
        return ("strike", "Too weak to strike.", "gray")

    def regenerate(self):
        self.energy += 7
        return ("regenerate", "Feeding... fragments of memory return.", "orange")

    def status(self):
        return f"Coils: {self.coils}, Energy: {self.energy}"


class JRXXGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jaraxxus Visualization")
        self.canvas = tk.Canvas(root, bg="black", width=800, height=600)
        self.canvas.pack()

        self.serpent = Serpent(coils=7)
        self.memory_icons = [
            "☠", "⚙", "✶", "⛧", "⦿", "⟁", "⟟", "⛩", "⦻", "⍊"
        ]

        self.display_sequence()
        self.regenerate_btn = tk.Button(root, text="Regenerate", command=self.display_sequence)
        self.regenerate_btn.pack()

    def draw_vector_shape(self, color):
        shape_type = random.choice(["zigzag", "circle", "glyph"])
        x, y = random.randint(50, 700), random.randint(50, 500)
        if shape_type == "zigzag":
            points = [x, y, x+10, y-10, x+20, y]
            self.canvas.create_line(points, fill=color, width=2)
        elif shape_type == "circle":
            self.canvas.create_oval(x, y, x+30, y+30, outline=color, width=2)
        elif shape_type == "glyph":
            icon = random.choice(self.memory_icons)
            self.canvas.create_text(x, y, text=icon, fill=color, font=("Consolas", 20, "bold"))

    def display_sequence(self):
        self.canvas.delete("all")

        actions = [self.serpent.writhe, self.serpent.hiss, self.serpent.strike, self.serpent.regenerate]
        y = 50
        for action in actions:
            _, text, color = action()
            x = random.randint(20, 600)
            font_size = random.randint(12, 24)
            self.canvas.create_text(x, y, text=text, fill=color, font=("Consolas", font_size, "bold"))
            self.draw_vector_shape(color)
            y += 60

        status_text = self.serpent.status()
        self.canvas.create_text(100, 580, text=status_text, fill="deeppink", anchor="w", font=("Consolas", 12, "bold"))


if __name__ == '__main__':
    root = tk.Tk()
    app = JRXXGUI(root)
    root.mainloop()
