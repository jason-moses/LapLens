import os
import fastf1
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

class Report:
    def __init__(self):
        self.slide_number = 1
        if self.slide_number == 1:
            self.slide1 = Tk()
            self.slide1.title("Race Overview")
            self.slide1.state("zoomed")
            self.slide1.update_idletasks()
            self.screen_width = self.slide1.winfo_screenwidth()
            self.screen_height = self.slide1.winfo_screenheight()
            self.bg_image_raw = Image.open("Slide1.jpeg")
            self.bg_image = ImageTk.PhotoImage(self.bg_image_raw)
            self.bg_image_resized = self.bg_image_raw.resize((self.screen_width, self.screen_height),
                                                             Image.Resampling.LANCZOS)
            self.bg_label = Label(self.slide1, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.button1 = Button(
                self.slide1,
                text="Continue",
                font=("Arial", 14, "bold"),
                bg="white",
                fg="black",
                padx=20,
                pady=10,
                command=self.on_continue)
            self.button1.place(x=0.98 * self.screen_width, y=0.9 * self.screen_height, anchor="se")


    def on_continue(self):
            self.slide1.destroy()
            self.slide_number += 1
            print(self.slide_number)
