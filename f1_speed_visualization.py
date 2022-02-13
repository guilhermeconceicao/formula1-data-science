
import fastf1
import numpy as np
import matplotlib as mpl

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

# get arguments
year = int(input('Race year:'))
gp = input('Grand Prix:')
event = input('Event (FP1, FP2, FP3, Q, SQ, R):')
driver = input('Driver:')
colormap = mpl.cm.plasma

# enable cache
fastf1.Cache.enable_cache('..\Formula1.DataScience\CacheF1') 

# load a session and laps
session = fastf1.get_session(year, gp, event) 
laps = session.load_laps(with_telemetry=True)
lap = laps.pick_driver(driver).pick_fastest()

# get telemetry data
x = lap.telemetry['X']              # values for x-axis
y = lap.telemetry['Y']              # values for y-axis
color = lap.telemetry['Speed']      # value to base color gradient on

# now, we create a set of line segments so that we can color them individually. 
# this creates the points as a N x 1 x 2 array so that we can stack points together easily to get the segments. 
# the segments array for line collection needs to be (numlines) x (points per line) x 2 (for x and y)
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# we create a plot with title and adjust some setting to make it look good.
fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle(f"{session.name} {year} - {lap['Driver']} - {lap['Team']} - Speed Visualization", size=24, y=0.97)

# adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')

# after this, we plot the data itself.
# create background track line
ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

# create a continuous norm to map from data points to colors
norm = plt.Normalize(color.min(), color.max())
lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

# set the values used for colormapping
lc.set_array(color)

# merge all line segments together
line = ax.add_collection(lc)

# finally, we create a color bar as a legend.
cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")

# show the plot
plt.show()