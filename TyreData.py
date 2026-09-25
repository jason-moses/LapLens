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
        self.slide2 = Tk()
        self.slide2.title("Tyre Analysis")
        self.slide2.state("zoomed")
        self.slide2["bg"] = "dark grey"
        self.session = fastf1.get_session(YEAR, RACE, SESSION)
        self.session.load()
        self.laps = self.session.laps
        self.drivers = self.session.drivers
        print(self.drivers)
        self.drivers = [self.session.get_driver(driver)["Abbreviation"] for driver in self.drivers]
        print(self.drivers)
        self.stints = self.laps[["Driver", "Stint", "Compound", "LapNumber"]]
        self.stints = self.stints.groupby(["Driver", "Stint", "Compound"])
        self.stints = self.stints.count().reset_index()
        self.stints = self.stints.rename(columns={"LapNumber": "StintLength"})
        print(self.stints)

        self.fig, self.ax = plt.subplots(figsize=(10, 5))

        for driver in self.drivers[:2]:
            self.driver_stints = self.stints.loc[self.stints["Driver"] == driver]

            self.previous_stint_end = 0
            for idx, row in self.driver_stints.iterrows():
                # each row contains the compound name and stint length
                # we can use these information to draw horizontal bars
                compound_color = fastf1.plotting.get_compound_color(row["Compound"],
                                                                    session=self.session)
                plt.barh(
                    y=driver,
                    width=row["StintLength"],
                    left=self.previous_stint_end,
                    color=compound_color,
                    edgecolor="black",
                    fill=True
                )

                self.previous_stint_end += row["StintLength"]

        plt.title("2021 Sao Paolo Grand Prix Tyre Strategies")
        plt.xlabel("Lap Number")
        plt.grid(False)
        # invert the y-axis so drivers that finish higher are closer to the top
        self.ax.invert_yaxis()
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        plt.legend(loc="upper left")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.slide2)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)
        self.canvas.draw()
        self.slide2.mainloop()

