import os
import fastf1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import gc
import warnings
from tkinter import *
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from adjustText import adjust_text

warnings.filterwarnings("ignore")


YEAR = 2021
RACE = "Brazil"
SESSION = "R"

class PlottingMachine:
    def __init__(self):
        popup = Tk()
        popup.title("Animation Settings")
        popup.configure(background="#2a2a2a")
        popup.geometry("250x260")
        speed_factor = IntVar(value=4)
        Label(popup, text="Select Animation Speed",
              font=("Arial", 12, "bold"), background="#2a2a2a", fg="red").pack(pady=10)

        speeds = [("1x", 1),
                  ("2x", 2),
                  ("4x", 4),
                  ("8x", 8),
                  ("16x", 16)]

        for text, value in speeds:
            Radiobutton(
                popup,
                text=text,
                variable=speed_factor,
                value=value,
                background="#2a2a2a",
                fg="red").pack(anchor="w", padx=30)

        Label(
            popup,
            text="Recommended speed: 4x",
            font=("Arial", 9, "italic"),
            background="#2a2a2a",
            fg="red"
        ).pack(pady=10)

        Button(
            popup,
            text="Continue",
            command=popup.destroy,
            background="white").pack(pady=15)

        popup.mainloop()
        self.speed_factor = speed_factor.get()

        self.cache_dir = os.path.expanduser('-f1_cache')
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            print("Successfully created the cache directory")

        else:
            print("Cache directory already exists")

        fastf1.Cache.enable_cache(self.cache_dir)
        print("Libraries Installed and Imported Successfully")

        print(f"\nLoading {YEAR} {RACE} GP - {SESSION} session")
        self.session = fastf1.get_session(YEAR, RACE, SESSION)
        self.session.load()

        self.circuit_info = self.session.event
        print(f"\n{'=' * 60}")
        print(f"CIRCUIT INFORMATION")
        print(f"\n{'=' * 60}")
        print(f"Event: {self.circuit_info['EventName']}")
        print(f"Location: {self.circuit_info['Location']}")
        print(f"Country: {self.circuit_info['Country']}")
        print(f"Circuit: {self.circuit_info['OfficialEventName']}")
        print(f"Date: {self.circuit_info['EventDate']}")
        print(f"\n{'=' * 60}")

        self.DRIVER_1 = 'VER'
        self.DRIVER_2 = 'HAM'

        self.driver1_fastest = self.session.laps.pick_drivers(self.DRIVER_1).pick_fastest()
        self.driver2_fastest = self.session.laps.pick_drivers(self.DRIVER_2).pick_fastest()

        self.driver1_name = self.driver1_fastest['Driver']
        self.driver2_name = self.driver2_fastest['Driver']

        self.driver1_laps = self.session.laps.pick_drivers(self.DRIVER_1)
        self.driver2_laps = self.session.laps.pick_drivers(self.DRIVER_2)

        self.lap_data = []

        for i, lap in enumerate(self.driver1_laps.iterlaps(), 1):
            self.lap_data.append({
                'Lap': i,
                f'{self.DRIVER_1} Time': lap[1]['LapTime'].total_seconds(),
                f'{self.DRIVER_1} Fastest': '*' if lap[1]['LapTime'] == self.driver1_fastest['LapTime'] else ''
            })

        for i, lap in enumerate(self.driver2_laps.iterlaps(), 1):
            if i <= len(self.lap_data):
                self.lap_data[i - 1][f'{self.DRIVER_2} Time'] = lap[1]['LapTime'].total_seconds()
                self.lap_data[i - 1][f'{self.DRIVER_2} Fastest'] = '*' if lap[1]['LapTime'] == self.driver2_fastest['LapTime'] else ''

            else:
                self.lap_data.append({
                    'Lap': i,
                    f'{self.DRIVER_1} Time': None,
                    f'{self.DRIVER_1} Fastest': '',
                    f'{self.DRIVER_2} Time': lap[1]['LapTime'],
                    f'{self.DRIVER_2} Fastest': '*' if lap[1]['LapTime'] == self.driver2_fastest['LapTime'] else ''
                })

        self.lap_times_df = pd.DataFrame(self.lap_data)
        print("\n" + "=" * 80)
        print(f"LAP TIMES COMPARISON - {self.DRIVER_1} vs {self.DRIVER_2}")
        print("=" * 80)
        print(self.lap_times_df.to_string(index=False))
        print("=" * 80)

        print(f"\n{self.DRIVER_1} Fastest Lap: {self.driver1_fastest['LapTime']}")
        print(f"{self.DRIVER_2} Fastest Lap: {self.driver2_fastest['LapTime']}")

        self.driver_1_laps_df = self.session.laps.pick_drivers(self.DRIVER_1)
        self.driver_2_laps_df = self.session.laps.pick_drivers(self.DRIVER_2)

        self.all_driver1_telemetry = []
        for lap_number, lap_object in self.driver_1_laps_df.iterlaps():
            self.lap_telemetry1 = lap_object.get_telemetry()
            self.lap_telemetry1['LapNum'] = lap_number - 70
            self.lap_telemetry1['Tyre'] = lap_object['Compound']
            self.lap_telemetry1['Position'] = lap_object['Position']
            self.all_driver1_telemetry.append(self.lap_telemetry1)

        self.driver1_tel = pd.concat(self.all_driver1_telemetry)

        self.all_driver2_telemetry = []
        for lap_number, lap_object in self.driver_2_laps_df.iterlaps():
            self.lap_telemetry2 = lap_object.get_telemetry()
            self.lap_telemetry2['LapNum'] = lap_number + 1
            self.lap_telemetry2['Tyre'] = lap_object['Compound']
            self.lap_telemetry2['Position'] = lap_object['Position']
            self.all_driver2_telemetry.append(self.lap_telemetry2)

        self.driver2_tel = pd.concat(self.all_driver2_telemetry)

        self.SAMPLE_RATE = 1
        self.driver1_tel = self.driver1_tel.iloc[::self.SAMPLE_RATE].reset_index(drop=True)
        self.driver2_tel = self.driver2_tel.iloc[::self.SAMPLE_RATE].reset_index(drop=True)

        self.driver1_x = 0.8*self.driver1_tel['X'].values-1000
        self.driver1_y = 0.8*self.driver1_tel['Y'].values
        self.driver1_speed = self.driver1_tel['Speed'].values
        self.driver1_drs = self.driver1_tel['DRS'].values
        self.driver1_gear = self.driver1_tel['nGear'].values
        self.driver1_bis = self.driver1_tel['Brake'].values.astype(int)
        self.driver1_lap_num = self.driver1_tel['LapNum'].values
        self.driver1_tyre = self.driver1_tel['Tyre'].values
        self.driver1_position = self.driver1_tel['Position'].values

        self.driver2_x = 0.8*self.driver2_tel['X'].values-1000
        self.driver2_y = 0.8*self.driver2_tel['Y'].values
        self.driver2_speed = self.driver2_tel['Speed'].values
        self.driver2_drs = self.driver2_tel['DRS'].values
        self.driver2_gear = self.driver2_tel['nGear'].values
        self.driver2_bis = self.driver2_tel['Brake'].values.astype(int)
        self.driver2_lap_num = self.driver2_tel['LapNum'].values
        self.driver2_tyre = self.driver2_tel['Tyre'].values
        self.driver2_position = self.driver2_tel['Position'].values

        self.driver1_time = self.driver1_tel['SessionTime'].dt.total_seconds().values
        self.driver2_time = self.driver2_tel['SessionTime'].dt.total_seconds().values

        self.driver1_time = self.driver1_time - self.driver1_time[0]
        self.driver2_time = self.driver2_time - self.driver2_time[0]

        print(f"\nTelemetry data extracted for {self.DRIVER_1} and {self.DRIVER_2}")
        print(f" - {self.DRIVER_1}: {len(self.driver1_x)*18} data points collected")
        print(f" - {self.DRIVER_2}: {len(self.driver2_x)*18} data points collected")

        gc.collect()

        print("\n" + "=" * 60)
        print("CREATING ANIMATION (OPTIMIZED FOR LOW MEMORY)...")
        print("=" * 60)

        # OPTIMIZATION: Reduced figure size
        self.fig, self.ax = plt.subplots(figsize=(10, 8), dpi=60)
        self.fig.patch.set_facecolor('#1a1a1a')
        self.ax.set_facecolor('#2a2a2a')
        self.xmin = -4754
        self.xmax = 2003
        self.ymin = -5893
        self.ymax = 5487
        print(self.xmin, self.xmax, self.ymin, self.ymax)
        self.ax.set_xlim(1.2*self.xmin, 1.2*self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)

        # OPTIMIZATION: Sample track background points (every 2nd point)
        self.ax.plot(self.driver1_x, self.driver1_y,
                color='lightgrey', alpha=0.5, linewidth=16,
                linestyle='-',zorder=2)
        self.ax.plot(self.driver2_x, self.driver2_y,
                color='black', alpha=0.9, linewidth=10,
                linestyle='-',zorder=2)

        # Initialize moving elements
        self.driver1_point, = self.ax.plot([], [], 'o', color='#ed1e36', markersize=12,
                                 label=f'{self.DRIVER_1}', markeredgecolor='white',
                                 markeredgewidth=1.5,zorder=3)
        self.driver2_point, = self.ax.plot([], [], 'o', color='#00a19b', markersize=12,
                                 label=f'{self.DRIVER_2}', markeredgecolor='white',
                                 markeredgewidth=1.5,zorder=3)

        # OPTIMIZATION: Shorter trails
        self.driver1_trail, = self.ax.plot([], [], color='#ed1e36', alpha=0.5, linewidth=2.5,zorder=3)
        self.driver2_trail, = self.ax.plot([], [], color='#00a19b', alpha=0.5, linewidth=2.5,zorder=3)

        # Time display
        self.time_text = self.ax.text(0.17, 0.98, '', transform=self.ax.transAxes,
                            fontsize=25, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='black', alpha=0.8),
                            color='white', fontfamily='monospace')
        self.fastest_lap1 = self.ax.text(0.08,0.67,'',
                                         transform=self.ax.transAxes,color='#ed1e36',fontsize=25,
                                         style='italic', fontname='Impact')
        self.fastest_lap2 = self.ax.text(0.665,0.67,'',
                                         transform=self.ax.transAxes,color='#00a19b',fontsize=25,
                                         style='italic', fontname='Impact')

        self.speed_text1 = self.ax.text(0.095, 0.41, '',
                                        transform=self.ax.transAxes,color='#ed1e36',fontsize=50,
                                        style='italic', fontname='Impact')
        self.speed_text2 = self.ax.text(0.68, 0.41, '',
                                        transform=self.ax.transAxes,color='#00a19b',fontsize=50,
                                        style='italic', fontname='Impact')
        self.drs_text1 = self.ax.text(0.085, 0.32, '',
                                      transform=self.ax.transAxes,color='#ed1e36',fontsize=25,
                                      style='italic', fontname='Impact')
        self.drs_text2 = self.ax.text(0.67, 0.32, '',
                                      transform=self.ax.transAxes,color='#00a19b',fontsize=25,
                                      style='italic', fontname='Impact')
        self.gear_text1 = self.ax.text(0.085, 0.5,'',
                                       transform=self.ax.transAxes,color='#ed1e36',fontsize=50,
                                       style='italic', fontname='Impact')
        self.gear_text2 = self.ax.text(0.67, 0.5, '',
                                       transform=self.ax.transAxes,color='#00a19b',fontsize=50,
                                       style='italic', fontname='Impact')
        self.brake_text1 = self.ax.text(0.197, 0.32, '',
                                        transform=self.ax.transAxes,color='#ed1e36',fontsize=25,
                                        style='italic', fontname='Impact')
        self.brake_text2 = self.ax.text(0.783, 0.32, '',
                                        transform=self.ax.transAxes,color='#00a19b',fontsize=25,
                                        style='italic', fontname='Impact')
        self.lap_text1 = self.ax.text(0.085, 0.59, '',
                                      transform=self.ax.transAxes,color='#ed1e36',fontsize=50,
                                      style='italic', fontname='Impact')
        self.lap_text2 = self.ax.text(0.67, 0.59, '',
                                      transform=self.ax.transAxes,color='#00a19b',fontsize=50,
                                      style='italic', fontname='Impact')
        self.tyre_text1 = self.ax.text(0.197, 0.225, '',
                                       transform=self.ax.transAxes,color='#ed1e36',fontsize=25,
                                       style='italic', fontname='Impact')
        self.tyre_text2 = self.ax.text(0.783, 0.225, '',
                                       transform=self.ax.transAxes,color='#00a19b',fontsize=25,
                                       style='italic', fontname='Impact')
        self.position_text1 = self.ax.text(0.09, 0.23, '',
                                           transform=self.ax.transAxes,color='#ed1e36',fontsize=50,
                                           style='italic', fontname='Impact',
                                           bbox=dict(boxstyle='round', facecolor='black', alpha=1))
        self.position_text2 = self.ax.text(0.675, 0.23, '',
                                           transform=self.ax.transAxes,color='#00a19b',fontsize=50,
                                           style='italic', fontname='Impact',
                                           bbox=dict(boxstyle='round', facecolor='black', alpha=1))
        self.texts = []
        self.texts.append(self.speed_text1)
        self.texts.append(self.speed_text2)
        self.texts.append(self.gear_text1)
        self.texts.append(self.gear_text2)
        self.texts.append(self.drs_text1)
        self.texts.append(self.drs_text2)
        self.texts.append(self.brake_text1)
        self.texts.append(self.brake_text2)
        self.texts.append(self.lap_text1)
        self.texts.append(self.lap_text2)
        self.texts.append(self.tyre_text1)
        self.texts.append(self.tyre_text2)
        self.texts.append(self.position_text1)
        self.texts.append(self.position_text2)
        adjust_text(self.texts, objects=[self.ax],arrowprops=dict(arrowstyle='-',color='grey'))

        # Styling
        self.ax.set_xlabel('X Position (m)', fontsize=10, color='white')
        self.ax.set_ylabel('Y Position (m)', fontsize=10, color='white')
        self.ax.axis('off')
        self.ax.tick_params(colors='white', labelsize=9)
        self.ax.legend(loc='upper right',
                  bbox_to_anchor=(0.7,1), fontsize=20, markerscale=2, facecolor='black',
                  edgecolor='white', labelcolor='white')
        self.ax.grid(True, alpha=0.2, color='white')
        self.ax.set_box_aspect(0.5625)

        # OPTIMIZATION: Lower FPS and frame count
          # Reduced from 30
        self.max_time = max(self.driver1_time[-1], self.driver2_time[-1])
        self.total_frames = 48384
        self.FPS = self.total_frames / self.max_time

        print(f"Animation settings:")
        print(f"  - FPS: {self.FPS} (lower = less memory)")
        print(f"  - Total frames: {self.total_frames}")
        print(f"  - Duration: {self.max_time:.2f} seconds")
        print("\nBuilding animation frames (this is faster with optimizations)...")
        self.root = Tk()
        self.root.state('zoomed')
        self.bg_data = plt.imread("LapLens_BG.png")
        self.ax.imshow(self.bg_data, aspect='equal',zorder=0,
                       extent=[2.5*self.xmin+1000, 2.5*self.xmax+1000, self.ymin-200, self.ymax+200])
        self.ani = FuncAnimation(self.fig, self.animate, frames=range(0, self.total_frames, self.speed_factor),
                             interval=600/self.FPS, blit=True, repeat=False)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.root.mainloop()

    def get_position(self,time_val, time_array,
                     x_array, y_array,
                     speed_array, drs_array,
                     gear_array, brake_array,
                     lap_num_array, tyre_array,
                     position_array):
        """Interpolate position at given time"""
        if time_val > time_array[-1]:
            return (x_array[-1], y_array[-1],
                    speed_array[-1], drs_array[-1],
                    gear_array[-1], brake_array[-1],
                    lap_num_array[-1], tyre_array[-1],
                    position_array[-1])
        idx = np.searchsorted(time_array, time_val)
        if idx == 0:
            return (x_array[0], y_array[0],
                    speed_array[0], drs_array[0],
                    gear_array[0], brake_array[0],
                    lap_num_array[0], tyre_array[0],
                    position_array[0])
        if idx >= len(time_array):
            return (x_array[-1], y_array[-1],
                    speed_array[-1], drs_array[-1],
                    gear_array[-1], brake_array[-1],
                    lap_num_array[-1], tyre_array[-1],
                    position_array[-1])

        # Linear interpolation
        t1, t2 = time_array[idx - 1], time_array[idx]
        alpha = (time_val - t1) / (t2 - t1) if t2 != t1 else 0
        x = x_array[idx - 1] + alpha * (x_array[idx] - x_array[idx - 1])
        y = y_array[idx - 1] + alpha * (y_array[idx] - y_array[idx - 1])
        speed = speed_array[idx - 1] + alpha * (speed_array[idx] - speed_array[idx - 1])
        drs = round(drs_array[idx - 1] + alpha * (drs_array[idx] - drs_array[idx - 1]))
        gear = round(gear_array[idx - 1] + alpha * (gear_array[idx] - gear_array[idx - 1]))
        brake = round(brake_array[idx - 1] + alpha * (brake_array[idx] - brake_array[idx - 1]))
        lap = round(lap_num_array[idx-1] + alpha * (lap_num_array[idx] - lap_num_array[idx - 1]))
        position = round(position_array[idx - 1] + alpha * (position_array[idx - 1] - position_array[idx - 1]))
        if alpha <= 0.5:
            tyre = tyre_array[idx - 1]
        else:
            tyre = tyre_array[idx]
        return (x, y,
                speed, drs,
                gear, brake,
                lap, tyre,
                position)

    def animate(self,frame):
        """Animation function (optimized)"""
        self.current_time = self.driver1_time[frame]

        # Get positions
        x1, y1, speed1, drs1, gear1, b1, l1, ty1, p1 = self.get_position(self.current_time, self.driver1_time,
                                                 self.driver1_x, self.driver1_y,
                                                 self.driver1_speed, self.driver1_drs,
                                                 self.driver1_gear, self.driver1_bis,
                                                 self.driver1_lap_num, self.driver1_tyre,
                                                 self.driver1_position)
        x2, y2, speed2, drs2, gear2, b2, l2, ty2, p2 = self.get_position(self.current_time, self.driver2_time,
                                           self.driver2_x, self.driver2_y,
                                           self.driver2_speed, self.driver2_drs,
                                           self.driver2_gear, self.driver2_bis,
                                           self.driver2_lap_num, self.driver2_tyre,
                                           self.driver2_position)

        # Update points
        self.driver1_point.set_data([x1], [y1])
        self.driver2_point.set_data([x2], [y2])

        # OPTIMIZATION: Shorter trail (30 points instead of 100)
        self.trail_length = 10
        self.start_frame = max(0, frame - self.trail_length)

        trail1_x, trail1_y = [], []
        trail2_x, trail2_y = [], []

        # OPTIMIZATION: Sample trail points (every 2nd)
        for f in range(self.start_frame, frame + 1):
            t = self.driver1_time[f]
            tx1, ty1, tvel1, self.d1, self.ng1, self.bis1, self.lap1, self.tyres1, self.pos1 = self.get_position(t, self.driver1_time,
                                                    self.driver1_x, self.driver1_y,
                                                    self.driver1_speed, self.driver1_drs,
                                                    self.driver1_gear, self.driver1_bis,
                                                    self.driver1_lap_num, self.driver1_tyre,
                                                    self.driver1_position)
            tx2, ty2, tvel2, self.d2, self.ng2, self.bis2, self.lap2, self.tyres2, self.pos2 = self.get_position(t, self.driver2_time,
                                                    self.driver2_x, self.driver2_y,
                                                    self.driver2_speed, self.driver2_drs,
                                                    self.driver2_gear, self.driver2_bis,
                                                    self.driver2_lap_num, self.driver2_tyre,
                                                    self.driver2_position)
            trail1_x.append(tx1)
            trail1_y.append(ty1)
            trail2_x.append(tx2)
            trail2_y.append(ty2)

        self.driver1_trail.set_data(trail1_x, trail1_y)
        self.driver2_trail.set_data(trail2_x, trail2_y)

        # Update time display
        self.hours = math.floor(round(self.current_time,2)/3600)
        self.minutes = math.floor(round(self.current_time,2)/60) - 60*self.hours
        self.seconds = round(self.current_time%60)
        self.time_text.set_text(f'Time: {self.hours}:{self.minutes}:{self.seconds}')
        self.fastest_lap1.set_text("1:12.486")
        self.fastest_lap2.set_text("1:11.982")

        self.speed_text1.set_text(round(speed1))
        self.speed_text2.set_text(round(speed2))
        if self.d1 == 1:
            self.drs_text1.set_text("IN")
        else:
            self.drs_text1.set_text("OUT")
        if self.d2 == 1:
            self.drs_text2.set_text("IN")
        else:
            self.drs_text2.set_text("OUT")
        self.gear_text1.set_text(round(gear1))
        self.gear_text2.set_text(round(gear2))
        if self.bis1 == 0:
            self.brake_text1.set_text("ON")
        else:
            self.brake_text1.set_text("")
        if self.bis2 == 0:
            self.brake_text2.set_text("ON")
        else:
            self.brake_text2.set_text("")
        self.lap_text1.set_text(self.lap1)
        self.lap_text2.set_text(self.lap2)
        self.tyre_text1.set_text(self.tyres1[0])
        self.tyre_text2.set_text(self.tyres2[0])
        self.position_text1.set_text(f"P{self.pos1}")
        self.position_text2.set_text(f"P{self.pos2}")


        # Progress indicator (every 50 frames)
        if frame % 50 == 0:
            self.progress = (frame / self.total_frames) * 100
            print(f"  Rendering: {self.progress:.1f}% complete", end='\r')

        return (self.driver1_point, self.driver2_point,
                self.driver1_trail, self.driver2_trail,
                self.time_text, self.speed_text1, self.speed_text2,
                self.drs_text1, self.drs_text2,
                self.gear_text1, self.gear_text2,
                self.brake_text1, self.brake_text2,
                self.lap_text1, self.lap_text2,
                self.tyre_text1, self.tyre_text2,
                self.position_text1, self.position_text2,
                self.fastest_lap1, self.fastest_lap2)




