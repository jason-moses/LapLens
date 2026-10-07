#Note: This script was used to generate the graph for the Ultimate Track Map.
#      Due to high load time, this script is not run every time you initialise the
#      program. Instead, an image containing this graph is used.
#      I have attached the source code for this graph for reference purpose only.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap
import fastf1

session = fastf1.get_session(2021, 'Brazil','R')
session.load(telemetry=True, laps=True)

ver_laps = session.laps.pick_driver('VER')
ver_laps = ver_laps[ver_laps['Stint'] == 4].pick_quicklaps()

ham_laps = session.laps.pick_driver('HAM')
ham_laps = ham_laps[ham_laps['Stint'] == 4].pick_quicklaps()

ref_lap = session.laps.pick_fastest()
ref_tel = ref_lap.get_telemetry().add_distance()
max_distance = int(ref_tel['Distance'].max())
distance_grid = np.arange(0, max_distance+1, 1)
track_x = np.interp(distance_grid, ref_tel['Distance'], ref_tel['X'])
track_y = np.interp(distance_grid, ref_tel['Distance'], ref_tel['Y'])

def calculate_stint_avg_speed(driver_laps, dist_grid):
  all_speeds = []
  for index, lap in driver_laps.iterlaps():
    try:
      tel = lap.get_telemetry().add_distance()
      lap_speed = np.interp(dist_grid, tel['Distance'], tel['Speed'])
      all_speeds.append(lap_speed)
    except:
      pass
  return np.mean(all_speeds, axis=0)

ver_avg_speed = calculate_stint_avg_speed(ver_laps, distance_grid)
ham_avg_speed = calculate_stint_avg_speed(ham_laps, distance_grid)

faster_driver = np.where(ver_avg_speed > ham_avg_speed, 1, -1)

points = np.array([track_x, track_y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

fig, ax = plt.subplots(layout='tight')
fig.patch.set_facecolor("#110b2d")
ax.set_facecolor("#110b2d")
custom_colors = ['#03bfb5', '#ff0000']
cmap = ListedColormap(custom_colors)
lc = LineCollection(segments, norm=plt.Normalize(-1,1), cmap=cmap)
lc.set_array(faster_driver)
lc.set_linewidth(5)
line = ax.add_collection(lc)
ax.axis('equal')
ax.tick_params(labelleft=False, labelbottom=False, left=False, bottom=False)
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='HAM',
           markerfacecolor='#03bfb5', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='VER',
           markerfacecolor='#ff0000', markersize=10)
]
ax.legend(handles=legend_elements, loc='upper right')
plt.tight_layout()
plt.show()