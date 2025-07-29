# Project: JRXX (Jaraxxus)
# Description: Experimental code logic exploration from JRXX repo
# Notes: Contextual window opened via o4-mini boost

# Let's start with a base context pulled from the Snake.py artifact
# and progressively refine or mutate it into new behavior forms.

import tkinter as tk
import random

class LiquidGlyph:
    def __init__(self, x, y, dx, dy, color, entropy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.entropy = entropy

    def move(self):
        self.x += self.dx * self.entropy
        self.y += self.dy * self.entropy
        self.dy += 0.05  # gravity simulation
        if self.y > 580:
            self.y = 580
            self.dy *= -0.7  # bounce with damping
            self.entropy *= 0.95

    def draw(self, canvas):
        canvas.create_oval(self.x, self.y, self.x+5, self.y+5, fill=self.color, outline="")

class LiquidCycle:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack()
        self.glyphs = []
        self.animate()

    def animate(self):
        self.canvas.delete("all")

        if random.random() < 0.3:
            self.glyphs.append(LiquidGlyph(
                x=400,
                y=0,
                dx=random.uniform(-1, 1),
                dy=0,
                color=random.choice(["cyan", "magenta", "lime", "white"]),
                entropy=random.uniform(0.7, 1.3)
            ))

        for glyph in self.glyphs:
            glyph.move()
            glyph.draw(self.canvas)

        self.canvas.after(30, self.animate)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Recursive Glyph Invocation")
    app = LiquidCycle(root)
    root.mainloop()
