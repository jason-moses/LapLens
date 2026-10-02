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

class TyreData:
    def __init__(self):
        self.slide2 = Toplevel()
        self.slide2.title("Tyre Stint Analysis")
        self.slide2.state("zoomed")
        self.slide2.update_idletasks()
        self.screen_width = self.slide2.winfo_screenwidth()
        self.screen_height = round(0.9*self.slide2.winfo_screenheight())
        self.bg_image_raw = Image.open("Tyre Stints.png")
        self.bg_image = ImageTk.PhotoImage(self.bg_image_raw, master=self.slide2)
        self.bg_image_resized = self.bg_image_raw.resize((self.screen_width, self.screen_height),
                                                         Image.Resampling.LANCZOS)
        self.final_image = ImageTk.PhotoImage(self.bg_image_resized)
        self.bg_label = Label(self.slide2, image=self.final_image)
        self.bg_label.place(x=0, y=10, relwidth=1, relheight=1)
        self.button1 = Button(
            self.slide2,
            text="Continue",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black",
            padx=20,
            pady=10,
            command=self.on_continue)
        self.button1.place(x=0.98 * self.screen_width, y=0.98 * self.screen_height, anchor="se")
        self.slide2.mainloop()


    def on_continue(self):
            self.slide2.withdraw()

