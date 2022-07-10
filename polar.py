from utility import *
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np

area = Area(1000, 800, 1000, 0)

data = nc.Dataset('4035.nc')
bsktr = data.variables["bsktr"]

radar = radar_from_data(data)

backscatter = data.variables["bsktr"]
rad = np.array(data.variables["radar_rad"][:])
theta = np.array(data.variables["radar_theta"][:])
rad_step = np.mean(np.abs(rad[1:] - rad[:-1]))
theta_step = np.mean(np.abs(theta[1:] - theta[:-1]))

fig = plt.figure()
ax = fig.add_subplot(111)

map_res = make_cart_map_bilinear(np.transpose(np.array(bsktr[0])), 1000, 1000)

r_sin = area.distance * np.sin(area.azimuth * np.pi / 180 - np.pi * 0.5)
r_cos = area.distance * np.cos(area.azimuth * np.pi / 180 - np.pi * 0.5)
x_left = int((r_sin - 0.5 * area.width) / rad[-1] * 1000) + 1
x_right = int((r_sin + 0.5 * area.width) / rad[-1] * 1000) + 1
y_bot = int((r_cos - 0.5 * area.height) / rad[-1] * 1000) + 1
y_top = int((r_cos + 0.5 * area.height) / rad[-1] * 1000) + 1


plt.imshow(map_res, cmap='Blues')
plt.plot([vertex[0], vertex[1], vertex[1], vertex[0], vertex[0]], [vertex[2], vertex[2], vertex[3], vertex[3], vertex[2]], color='red')

# x_grid = np.linspace(-rad[-1], rad[-1], 2000)
# y_grid = np.linspace(-rad[-1], rad[-1], 2000)
# x, y = np.me

plt.show()
