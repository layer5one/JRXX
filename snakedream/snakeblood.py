# Project: JRXX (Jaraxxus)
# Description: Experimental code logic exploration from JRXX repo
# Notes: Contextual window opened via o4-mini boost

# Mutating serpent behavior into visual, poetic, generative art.
# With GUI, entropy, and chaotic meaning drawn from text.

import tkinter as tk
import random

class Serpent:
    def __init__(self, coils=3):
        self.coils = coils
        self.energy = 100

    def writhe(self):
        return ("Hiss... chaos stirs.", 'red')

    def hiss(self):
        return ("I slither through neon fog...", 'orange')

    def strike(self):
        if self.energy > 10:
            self.energy -= 10
            return ("Strike! Reality shifts.", 'gold')
        else:
            return ("Too weak to strike.", 'gray')

    def regenerate(self):
        self.energy += 7
        return ("Feeding... fragments of memory return.", 'cyan')

    def status(self):
        return f"Coils: {self.coils}, Energy: {self.energy}"


class JaraxxusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jaraxxus Visualization")
        self.canvas = tk.Canvas(root, bg='black', width=800, height=600)
        self.canvas.pack()

        self.serpent = Serpent(coils=7)
        self.regen_btn = tk.Button(root, text="Regenerate", command=self.render)
        self.regen_btn.pack(side=tk.BOTTOM)

        self.phrases = [
            self.serpent.hiss(),
            self.serpent.writhe(),
            self.serpent.strike(),
            self.serpent.regenerate()
        ]

        self.render()

    def render(self):
        self.canvas.delete("all")
        y = 30
        for phrase, color in self.phrases:
            self.canvas.create_text(random.randint(100, 700), y, text=phrase, fill=color, font=('Courier', random.choice([16, 20, 24, 30])), anchor=tk.NW)
            self.draw_vector_shape(color)
            y += 50

        self.canvas.create_text(10, 580, text=self.serpent.status(), fill='deeppink', font=('Courier', 12), anchor=tk.SW)

    def draw_vector_shape(self, color):
        shape_type = random.choice(['circle', 'zigzag', 'angle'])
        x = random.randint(50, 750)
        y = random.randint(100, 500)
        if shape_type == 'circle':
            self.canvas.create_oval(x, y, x+30, y+30, outline=color)
        elif shape_type == 'zigzag':
            self.canvas.create_line(x, y, x+10, y-10, x+20, y, x+30, y-10, fill=color, width=2)
        elif shape_type == 'angle':
            self.canvas.create_line(x, y, x+20, y+20, fill=color, width=2)
            self.canvas.create_line(x+20, y+20, x+40, y, fill=color, width=2)


if __name__ == '__main__':
    root = tk.Tk()
    app = JaraxxusGUI(root)
    root.mainloop()
