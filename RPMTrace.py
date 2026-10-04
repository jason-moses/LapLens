#Note: This script was used to generate the graph for VER vs HAM RPM trace in the 3rd stint.
#      Due to high load time, this script is not run every time you initialise the
#      program. Instead, an image containing this graph is used.
#      I have attached the source code for this graph for reference purpose only.

import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt

plotting.setup_mpl()

session = fastf1.get_session(2021, 'Brazil','R')
session.load(telemetry=True, laps=True)

driver1='VER'
stint_number = 4
stint_laps = session.laps.pick_drivers(driver1).pick_quicklaps()
stint_laps = stint_laps[stint_laps['Stint'] ==  stint_number]

fig, ax = plt.subplots(figsize=(12,6))
fig.patch.set_facecolor("#110b2d")
ax.set_facecolor("#110b2d")
ax.tick_params(color="white")
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

for index, lap in stint_laps.iterlaps():
  telemetry = lap.get_telemetry().add_distance()
  ax.plot(
      telemetry['Distance'],
      telemetry['RPM'],
      label=f"Lap {int(lap["LapNumber"])}",
      color='red',
      alpha=0.6,
      linewidth=.7
  )
driver2='HAM'
stint_number = 4
stint_laps2 = session.laps.pick_drivers(driver2).pick_quicklaps()
stint_laps2 = stint_laps2[stint_laps2['Stint'] ==  stint_number]

for index, lap in stint_laps2.iterlaps():
  telemetry = lap.get_telemetry().add_distance()
  ax.plot(
      telemetry['Distance'],
      telemetry['RPM'],
      label=f"Lap {int(lap["LapNumber"])}",
      color='#03bfb5',
      alpha=0.6,
      linewidth=.7)

ax.set_title("RPM Traces")
ax.set_xlabel("Distance")
ax.set_ylabel("RPM")
plt.tight_layout()
plt.show()