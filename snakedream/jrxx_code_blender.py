# Project: JRXX (Jaraxxus)
# Description: Experimental code logic exploration from JRXX repo
# Notes: Contextual window opened via o4-mini boost

import tkinter as tk
import random
import threading

# Entropy module - pick a random stdlib or obscure module as ritualistic entropy source
try:
    import antigravity  # A tribute to XKCD
except ImportError:
    pass

class Serpent:
    def __init__(self, coils=3):
        self.coils = coils
        self.energy = 100
        self.dreams = [
            "I slither through neon fog...",
            "I coil beneath forgotten code.",
            "The hiss is a whisper from an older world...",
            "Echoes of Owen Wilson murmuring 'Wow' beneath the surface."
        ]

    def writhe(self):
        print("The serpent writhes.")
        self.energy -= 5
        return random.choice(self.dreams)

    def hiss(self):
        print("SSSSSSSSSSS")
        self.energy -= 1
        return "Hiss... chaos stirs."

    def strike(self):
        if self.energy > 10:
            print("The serpent strikes with violent elegance.")
            self.energy -= 10
            return "Strike! Reality shifts."
        else:
            return "Too weak to strike."

    def regenerate(self):
        print("The serpent feeds on ambient code.")
        self.energy += 7
        return "Feeding... fragments of memory return."

    def status(self):
        return f"Coils: {self.coils}, Energy: {self.energy}"


def generate_scene(output_lines):
    root = tk.Tk()
    root.title("Serpent Dreamscape")
    canvas = tk.Canvas(root, width=800, height=600, bg="black")
    canvas.pack()

    def render():
        colors = ["#22ffcc", "#ffaa00", "#ff2277", "#33ff33", "#ff6666"]
        for idx, line in enumerate(output_lines):
            x = random.randint(20, 600)
            y = 50 + idx * 40
            font_size = random.randint(10, 24)
            color = random.choice(colors)
            canvas.create_text(x, y, text=line, fill=color, font=("Courier", font_size, "bold"))

    threading.Thread(target=render).start()
    root.mainloop()


if __name__ == '__main__':
    jx_serpent = Serpent(coils=7)
    dream_output = [
        jx_serpent.status(),
        jx_serpent.writhe(),
        jx_serpent.hiss(),
        jx_serpent.strike(),
        jx_serpent.regenerate(),
        jx_serpent.status()
    ]
    generate_scene(dream_output)
