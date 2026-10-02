#Note: This script was used to generate the graph for Verstappen's tyre degradation.
#      Due to high load time, this script is not run every time you initialise the
#      program. Instead, an image containing this graph is used.
#      I have attached the source code for this graph for reference purpose only.

import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt
from scipy.stats import linregress
import math

session = fastf1.get_session(2021, 'Brazil', 'R')
session.load()
fig, ax = plt.subplots()
fig.patch.set_facecolor("#110b2d")
ax.set_facecolor("#110b2d")
ax.tick_params(color="white")
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
for spine in ax.spines.values():
  spine.set_color("white")
driver = 'VER'
laps = session.laps.pick_driver(driver).pick_quicklaps()

lap_times = laps["LapTime"].dt.total_seconds()

for (stint, compound), stint_laps in laps.groupby(["Stint", "Compound"]):
  x = stint_laps["LapNumber"]
  y=stint_laps["LapTime"].dt.total_seconds()
  if len(x)<3:
    continue
  result = linregress(x,y)
  y_reg = result.slope*x + result.intercept
  angle = math.degrees(math.atan(result.slope))*5
  ax.plot(x,
          y_reg,
          color=plotting.get_compound_color(compound, session),
          linestyle = "--",
          linewidth = 2)
  ax.text((x.iloc[-1]+x.iloc[0])/2 - 5,
           y.iloc[-2]+0.5,
           f"{result.slope:+.3f} s/lap",
           rotation=angle,
           color="red",
           rotation_mode="anchor",
           va="center")

for compound in laps["Compound"].unique():
  compound_laps = laps[laps["Compound"] == compound]
  ax.scatter(compound_laps["LapNumber"],
            compound_laps["LapTime"].dt.total_seconds(),
            color = plotting.get_compound_color(compound, session),
            label=compound,
            s=30)
plt.xlabel("Lap Number")
plt.ylabel("Lap Time (s)")
plt.legend(title="Tyre Compound")
ax.grid(alpha=0)
plt.show()