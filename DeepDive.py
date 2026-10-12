import os
import fastf1
import fastf1.plotting
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import gc
import warnings
from tkinter import *
from PIL import Image, ImageTk
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from adjustText import adjust_text

warnings.filterwarnings("ignore")


YEAR = 2021
RACE = "Brazil"
SESSION = "R"

class DeepDive:
    def __init__(self):
        self.slide4 = Toplevel()
        self.slide4.title("Deep Dive")
        self.slide4.state("zoomed")
        self.slide4.update_idletasks()
        self.screen_width = self.slide4.winfo_screenwidth()
        self.screen_height = round(0.92*self.slide4.winfo_screenheight())
        self.bg_image_raw = Image.open("Deep Dive.png")
        self.bg_image = ImageTk.PhotoImage(self.bg_image_raw, master=self.slide4)
        self.bg_image_resized = self.bg_image_raw.resize((self.screen_width, self.screen_height),
                                                         Image.Resampling.LANCZOS)
        self.final_image = ImageTk.PhotoImage(self.bg_image_resized)
        self.bg_label = Label(self.slide4, image=self.final_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.button1 = Button(
            self.slide4,
            text="Continue",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black",
            padx=20,
            pady=10,
            command=self.on_continue)
        self.button1.place(x=0.98 * self.screen_width, y=0.99 * self.screen_height, anchor="se")
        self.slide4.mainloop()

    def on_continue(self):
        self.slide4.withdraw()
        from VERVSHAM import VerVSHam
        analysis = VerVSHam()
