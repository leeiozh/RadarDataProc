from utility import *
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np

area = Area(14000, 14000, 0, 0)

data = nc.Dataset('4035.nc')
bsktr = data.variables["bsktr"]

radar = radar_from_data(data)

backscatter = data.variables["bsktr"]
rad = np.array(data.variables["radar_rad"][:])
theta = np.array(data.variables["radar_theta"][:])

area_ind = vertex_indexes(area, rad, theta)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
# plt.imshow(bsktr[0][np.min(area_ind[:, 1]):np.max(area_ind[:, 1]), np.min(area_ind[:, 0]):np.max(area_ind[:, 0])], cmap='Blues')
plt.imshow(make_cart_map_smooth(np.transpose(np.array(bsktr[0])), 1500, 1500))

plt.show()
