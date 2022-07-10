from utility import *
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np

area = Area(7800 * 2, 7800 * 2, 0, 0)

resolution = 500

data = nc.Dataset('4035.nc')
bsktr = data.variables["bsktr"]

radar = radar_from_data(data)

backscatter = data.variables["bsktr"]
rad = np.array(data.variables["radar_rad"][:])
theta = np.array(data.variables["radar_theta"][:])
rad_step = np.mean(np.abs(rad[1:] - rad[:-1]))
theta_step = np.mean(np.abs(theta[1:] - theta[:-1]))

area2 = Area(500, 500, 1000, 30)
resolution2 = 2048

map_res, vertex_ = make_area(np.transpose(np.array(bsktr[0])), resolution, resolution, area, rad[-1])
map_res2, vertex = make_area(np.transpose(np.array(bsktr[0])), resolution2, resolution2, area2, rad[-1])

plt.subplot(211)

plt.imshow(map_res, cmap='Blues')

pole_x = np.array([vertex[0], vertex[1] + 1, vertex[1] + 1, vertex[0], vertex[0]])
pole_y = np.array([vertex[2], vertex[2], vertex[3] + 1, vertex[3] + 1, vertex[2]])

plt.plot(-pole_x + resolution, -pole_y + resolution, color='red')

plt.subplot(212)

plt.imshow(map_res2, cmap='Blues')

plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
cax = plt.axes([0.85, 0.1, 0.075, 0.8])
plt.colorbar(cax=cax)

plt.show()
