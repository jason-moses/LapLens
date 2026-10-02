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

class DegradationData:
    def __init__(self):
        self.slide3 = Toplevel()
        self.slide3.title("Tyre Degradation Analysis")
        self.slide3.state("zoomed")
        self.slide3.update_idletasks()
        self.screen_width = self.slide3.winfo_screenwidth()
        self.screen_height = round(0.9*self.slide3.winfo_screenheight())
        self.bg_image_raw = Image.open("Tyre Degradation.png")
        self.bg_image = ImageTk.PhotoImage(self.bg_image_raw, master=self.slide3)
        self.bg_image_resized = self.bg_image_raw.resize((self.screen_width, self.screen_height),
                                                         Image.Resampling.LANCZOS)
        self.final_image = ImageTk.PhotoImage(self.bg_image_resized)
        self.bg_label = Label(self.slide3, image=self.final_image)
        self.bg_label.place(x=0,y=10, relwidth=1, relheight=1)
        self.button1 = Button(
            self.slide3,
            text="Continue",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black",
            padx=20,
            pady=10,
            command=self.on_continue)
        self.button1.place(x=0.98*self.screen_width, y=0.99*self.screen_height, anchor="se")
        self.slide3.mainloop()

    def on_continue(self):
        self.slide3.withdraw()