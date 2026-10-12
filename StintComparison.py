
import warnings
from tkinter import *
from PIL import Image, ImageTk

warnings.filterwarnings("ignore")


YEAR = 2021
RACE = "Brazil"
SESSION = "R"

class StintComparison:
    def __init__(self):
        self.slide6 = Toplevel()
        self.slide6.title("Stint Comparison")
        self.slide6.state("zoomed")
        self.slide6.update_idletasks()
        self.screen_width = self.slide6.winfo_screenwidth()
        self.screen_height = round(0.92*self.slide6.winfo_screenheight())
        self.bg_image_raw = Image.open("Stint 3 vs Stint 4.png")
        self.bg_image = ImageTk.PhotoImage(self.bg_image_raw)
        self.bg_image_resized = self.bg_image_raw.resize((self.screen_width, self.screen_height),
                                                         Image.Resampling.LANCZOS)
        self.final_image = ImageTk.PhotoImage(self.bg_image_resized)
        self.bg_label = Label(self.slide6, image=self.final_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.button1 = Button(
            self.slide6,
            text="Continue",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black",
            padx=20,
            pady=10,
            command=self.on_continue)
        self.button1.place(x=0.98 * self.screen_width,y=0.98 * self.screen_height, anchor="se")
        self.slide6.mainloop()

    def on_continue(self):
        self.slide6.withdraw()