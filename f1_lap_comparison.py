
import matplotlib.pyplot as plt
import fastf1.plotting

# get arguments
year = int(input('Race year:'))
gp = input('Grand Prix:')
event = input('Event (FP1, FP2, FP3, Q, SQ, R):')
driver1 = input('Driver 1:')
driver2 = input('Driver 2:')

# enable cache
fastf1.Cache.enable_cache('..\Formula1.DataScience\CacheF1')
fastf1.plotting.setup_mpl()

# load a session and laps
session = fastf1.get_session(year, gp, event)
laps = session.load_laps(with_telemetry=True)

# load drivers fastest laps
driver1_lap = laps.pick_driver(driver1).pick_fastest()
driver2_lap = laps.pick_driver(driver2).pick_fastest()

# get telemetries and add distance
driver1_tel = driver1_lap.get_car_data().add_distance()
driver2_tel = driver2_lap.get_car_data().add_distance()

# plotting
driver1_team_color = fastf1.plotting.team_color(driver1_lap['Team'])
if driver1_lap['Team'] == driver2_lap['Team']:
    driver2_team_color = 'tab:pink'
else:
    driver2_team_color = fastf1.plotting.team_color(driver2_lap['Team'])

fig, ax = plt.subplots()
ax.plot(driver1_tel['Distance'], driver1_tel['Speed'], color=driver1_team_color, label=f"{driver1_lap['Driver']} ({driver1_lap['Compound']})")
ax.plot(driver2_tel['Distance'], driver2_tel['Speed'], color=driver2_team_color, label=f"{driver2_lap['Driver']} ({driver2_lap['Compound']})")

ax.set_xlabel('Distance in m')
ax.set_ylabel('Speed in km/h')

ax.legend()
plt.suptitle(f"Fastest Lap Comparison \n "
             f"{session.weekend.name} {session.weekend.year} {session.name}")

# show the plot
plt.show()