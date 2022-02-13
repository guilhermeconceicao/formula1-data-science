import matplotlib.pyplot as plt
import pandas as pd
import fastf1
import fastf1.plotting

from timple.timedelta import strftimedelta
from fastf1.core import Laps

# get arguments
year = int(input('Race year:'))
gp = input('Grand Prix:')
event = input('Event (FP1, FP2, FP3, Q, SQ, R):')

# enable cache
fastf1.Cache.enable_cache('..\Formula1.DataScience\CacheF1') 

# we only want support for timedelta plotting in this example
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

# load a session and laps
session = fastf1.get_session(year, gp, event) 
laps = session.load_laps()

# load drivers
drivers = pd.unique(laps['Driver'])

# get each drivers fastest lap and sort them by lap time and have pandas reindex them to number them nicely by starting position.
list_fastest_laps = list()
for driver in drivers:
    driver_fastest_lap = laps.pick_driver(driver).pick_fastest()
    list_fastest_laps.append(driver_fastest_lap)

fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

# subtract the pole lap from all other laps to get the time differences
pole_lap = fastest_laps.pick_fastest()
fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

# get teams colors
team_colors = list()
for index, lap in fastest_laps.iterlaps():
    color = fastf1.plotting.team_color(lap['Team'])
    team_colors.append(color)

# plot all the data
fig, ax = plt.subplots()
ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'], color=team_colors, edgecolor='grey')
ax.set_yticks(fastest_laps.index)
ax.set_yticklabels(fastest_laps['Driver'])

# show fastest at the top
ax.invert_yaxis()

# draw vertical lines behind the bars
ax.set_axisbelow(True)
ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

# title
lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')
plt.suptitle(f"{session.weekend.name} {session.weekend.year} {session.name}\n"
             f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']} - {pole_lap['Team']})")

# show the plot
plt.show()