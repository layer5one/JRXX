# Project: JRXX (Jaraxxus)
# Description: Experimental code logic exploration from JRXX repo
# Notes: Contextual window opened via o4-mini boost

# Serpent core mutation layer
# Now infused with glyph recursion and chaotic entropy pulses

import tkinter as tk
import random
import math

class Serpent:
    def __init__(self, coils=3):
        self.coils = coils
        self.energy = 100
        self.glyphs = []

    def writhe(self):
        print("The serpent writhes.")
        self.energy -= 5
        self.spawn_glyph("writhe")

    def hiss(self):
        print("SSSSSSSSSSS")
        self.energy -= 1
        self.spawn_glyph("hiss")

    def strike(self):
        if self.energy > 10:
            print("The serpent strikes with violent elegance.")
            self.energy -= 10
            self.spawn_glyph("strike")
        else:
            print("Too weak to strike.")

    def regenerate(self):
        print("The serpent feeds on ambient code.")
        self.energy += 7
        self.spawn_glyph("regenerate")

    def spawn_glyph(self, action):
        shape = random.choice(["circle", "triangle", "square", "spiral", "wave"])
        color = random.choice(["red", "cyan", "gold", "lime", "magenta"])
        self.glyphs.append((action, shape, color))

    def status(self):
        print(f"Coils: {self.coils}, Energy: {self.energy}, Glyphs: {len(self.glyphs)}")


# Ritual canvas for recursive glyph rendering
class GlyphCanvas:
    def __init__(self, serpent):
        self.serpent = serpent
        self.root = tk.Tk()
        self.root.title("Recursive Glyph Engine")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="black")
        self.canvas.pack()
        self.button = tk.Button(self.root, text="Feed the Serpent", command=self.trigger_cycle)
        self.button.pack()
        self.draw_loop()

    def draw_loop(self):
        self.canvas.delete("all")
        for i, (action, shape, color) in enumerate(self.serpent.glyphs[-10:]):
            x = random.randint(100, 700)
            y = random.randint(100, 500)
            size = 30 + (i * 5)
            if shape == "circle":
                self.canvas.create_oval(x, y, x + size, y + size, fill=color)
            elif shape == "square":
                self.canvas.create_rectangle(x, y, x + size, y + size, fill=color)
            elif shape == "triangle":
                self.canvas.create_polygon(x, y, x+size, y, x+size/2, y-size, fill=color)
            elif shape == "spiral":
                for j in range(10):
                    angle = j * math.pi / 5
                    dx = math.cos(angle) * j * 2
                    dy = math.sin(angle) * j * 2
                    self.canvas.create_oval(x+dx, y+dy, x+dx+2, y+dy+2, fill=color)
            elif shape == "wave":
                for j in range(5):
                    self.canvas.create_arc(x+j*size, y, x+(j+1)*size, y+size, start=0, extent=180, style=tk.ARC, outline=color)
        self.root.after(1000, self.draw_loop)

    def trigger_cycle(self):
        choice = random.choice([self.serpent.writhe, self.serpent.hiss, self.serpent.strike, self.serpent.regenerate])
        choice()


if __name__ == '__main__':
    jx_serpent = Serpent(coils=7)
    gui = GlyphCanvas(jx_serpent)
    gui.root.mainloop()
