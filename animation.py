from utility import *
from drawers import *
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

data = nc.Dataset('4035.nc')
bsktr = data.variables["bsktr"]

radar = radar_from_data(data)

backscatter = data.variables["bsktr"]

area2 = Area(3000, 3000, 3000, 90)
resolution2 = 4096

fig = plt.figure()

map_0, ver_0 = make_area(np.transpose(np.array(bsktr[0])), resolution2, resolution2, area2, radar.rad[-1])
im = draw_map(map_0, ver_0)


def init():
    im.set_data(make_area(np.transpose(np.array(bsktr[0])), resolution2, resolution2, area2, radar.rad[-1])[0])
    return [im]


def updatefig(t):
    im.set_array(make_area(np.transpose(np.array(bsktr[t])), resolution2, resolution2, area2, radar.rad[-1])[0])
    return [im]


ani = FuncAnimation(fig, updatefig, init_func=init, frames=50, interval=20000, blit=True)

writer = PillowWriter(fps=5)
ani.save("demo_wave_200.gif", writer=writer)
