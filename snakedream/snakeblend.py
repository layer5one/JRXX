# Project: JRXX (Jaraxxus)
# Description: Experimental code logic exploration from JRXX repo
# Notes: Contextual window opened via o4-mini boost

import tkinter as tk
import random

class Serpent:
    def __init__(self, coils=3):
        self.coils = coils
        self.energy = 100
        self.poetry = []

    def writhe(self):
        line = "I slither through neon fog..."
        self.energy -= 5
        self.poetry.append((line, 'orange'))
        return line

    def hiss(self):
        line = "Hiss... chaos stirs."
        self.energy -= 1
        self.poetry.append((line, 'red'))
        return line

    def strike(self):
        if self.energy > 10:
            line = "Strike! Reality shifts."
            self.energy -= 10
        else:
            line = "Too weak to strike."
        self.poetry.append((line, 'gold'))
        return line

    def regenerate(self):
        line = "Feeding... fragments of memory return."
        self.energy += 7
        self.poetry.append((line, 'cyan'))
        return line

    def status(self):
        return f"Coils: {self.coils}, Energy: {self.energy}"


class JaraxxusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jaraxxus Visualization")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack()
        self.serpent = Serpent(coils=7)
        self.render_poem()

        self.button = tk.Button(root, text="Regenerate", command=self.reset_and_generate)
        self.button.pack()

    def render_poem(self):
        self.canvas.delete("all")
        self.serpent.poetry.clear()

        actions = [self.serpent.writhe, self.serpent.hiss, self.serpent.strike, self.serpent.regenerate]
        for act in actions:
            act()

        y = 20
        for line, color in self.serpent.poetry:
            font_size = random.choice([14, 16, 20, 24])
            self.canvas.create_text(random.randint(100, 700), y, text=line, fill=color, font=("Consolas", font_size))
            y += font_size + 10
            self.create_vector_shape(line, color)

        # Show status
        self.canvas.create_text(100, 580, text=self.serpent.status(), fill="hot pink", font=("Courier", 12), anchor="w")

    def create_vector_shape(self, word, color):
        x, y = random.randint(100, 700), random.randint(100, 500)
        if "Hiss" in word:
            self.canvas.create_line(x, y, x+30, y-30, x+60, y, x+90, y-30, fill=color, width=3)
        elif "Strike" in word:
            self.canvas.create_line(x, y, x+50, y+50, x+25, y+75, fill=color, width=4)
        elif "Feeding" in word:
            self.canvas.create_oval(x, y, x+40, y+40, outline=color, width=2)
        elif "Fragments" in word:
            for _ in range(3):
                x1, y1 = x + random.randint(-20, 20), y + random.randint(-20, 20)
                self.canvas.create_polygon(x1, y1, x1+10, y1+5, x1+5, y1+15, fill=color)

    def reset_and_generate(self):
        self.serpent.energy = 100
        self.render_poem()


if __name__ == '__main__':
    root = tk.Tk()
    gui = JaraxxusGUI(root)
    root.mainloop()
