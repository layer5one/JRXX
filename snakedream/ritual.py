# Project: JRXX (Jaraxxus)
# Description: Experimental code logic exploration from JRXX repo
# Notes: Contextual window opened via o4-mini boost

# Let's start with a base context pulled from the Snake.py artifact
# and progressively refine or mutate it into new behavior forms.

import tkinter as tk
import random
import math

class Serpent:
    def __init__(self, coils=3):
        self.coils = coils
        self.energy = 100

    def writhe(self):
        print("The serpent writhes.")
        self.energy -= 5

    def hiss(self):
        print("SSSSSSSSSSS")
        self.energy -= 1

    def strike(self):
        if self.energy > 10:
            print("The serpent strikes with violent elegance.")
            self.energy -= 10
        else:
            print("Too weak to strike.")

    def regenerate(self):
        print("The serpent feeds on ambient code.")
        self.energy += 7

    def status(self):
        print(f"Coils: {self.coils}, Energy: {self.energy}")

# --- ELYSIAN Ritual Rendering ---
def random_color():
    return f"#{random.randint(50,255):02x}{random.randint(50,255):02x}{random.randint(50,255):02x}"

def orbital_position(cx, cy, radius, angle):
    rad = math.radians(angle)
    x = cx + radius * math.cos(rad)
    y = cy + radius * math.sin(rad)
    return x, y

def render_altar_scene():
    root = tk.Tk()
    root.title("ELYSIAN: Serpent Summoning")
    canvas = tk.Canvas(root, width=800, height=600, bg='black')
    canvas.pack()

    cx, cy = 400, 300

    # Altar Core
    canvas.create_oval(cx-30, cy-30, cx+30, cy+30, fill=random_color(), outline='white', width=3)

    # Glyph constellation
    glyph_list = ["☼", "⦿", "⚘", "⟁", "✴", "♒", "⛧", "҉", "⚙", "𓂀"]
    for i in range(10):
        angle = i * 36 + random.randint(-10,10)
        radius = 100 + random.randint(-30, 30)
        x, y = orbital_position(cx, cy, radius, angle)
        canvas.create_text(x, y, text=random.choice(glyph_list), fill=random_color(), font=('Courier', 20, 'bold'))

    # Regenerate button
    def rerun():
        canvas.delete("all")
        render_altar_scene()

    button = tk.Button(root, text="Regenerate Ritual", command=rerun)
    button.pack()

    root.mainloop()

if __name__ == '__main__':
    jx_serpent = Serpent(coils=7)
    jx_serpent.status()
    jx_serpent.writhe()
    jx_serpent.hiss()
    jx_serpent.strike()
    jx_serpent.regenerate()
    jx_serpent.status()
    render_altar_scene()
