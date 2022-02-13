import fastf1
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.collections import LineCollection
from matplotlib import cm

# get arguments
year = int(input('Race year:'))
gp = input('Grand Prix:')
event = input('Event (FP1, FP2, FP3, Q, SQ, R):')
driver = input('Driver:')

# enable cache
fastf1.Cache.enable_cache('..\Formula1.DataScience\CacheF1') 

# load a session and laps
session = fastf1.get_session(year, gp, event)
laps = session.load_laps(with_telemetry=True)

# load driver fastest lap
lap = laps.pick_driver(driver).pick_fastest()
tel = lap.get_telemetry()

# prepare the data for plotting by converting it to the appropriate numpy data types
x = np.array(tel['X'].values)
y = np.array(tel['Y'].values)

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
gear = tel['nGear'].to_numpy().astype(float)

# create a line collection. Set a segmented colormap and normalize the plot to full integer values of the colormap
cmap = cm.get_cmap('Paired')
lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
lc_comp.set_array(gear)
lc_comp.set_linewidth(4)

# create the plot
plt.gca().add_collection(lc_comp)
plt.axis('equal')
plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

title = plt.suptitle(
    f"Fastest Lap Gear Shift Visualization\n"
    f"{lap['Driver']} ({lap['Team']}) - {session.weekend.name} {session.weekend.year} {session.name}"
)

# add a colorbar to the plot. Shift the colorbar ticks by +0.5 so that they are centered for each color segment.
cbar = plt.colorbar(mappable=lc_comp, label="Gear", boundaries=np.arange(1, 10))
cbar.set_ticks(np.arange(1.5, 9.5))
cbar.set_ticklabels(np.arange(1, 9))

# show the plot
plt.show()