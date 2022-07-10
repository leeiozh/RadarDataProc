import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt


def polar_to_cartesian(rad, theta):
    theta *= np.pi / 180
    return rad * np.cos(theta), rad * np.sin(theta)


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

data = nc.Dataset('4035.nc')
bsktr = data.variables["bsktr"]

print(data.variables["radar_rad"].shape)

t = 0

rad = np.array(data.variables["radar_rad"][:])
theta = np.array(data.variables["radar_theta"][:])

rad_step = np.mean(np.abs(rad[1:] - rad[:-1]))
theta_step = np.mean(np.abs(theta[1:] - theta[:-1]))

plt.imshow(bsktr[t], cmap='Blues')

# ax.scatter(data.variables['radar_time'][:], data.variables['radar_lat'][:])
# ax.plot(data.variables['radar_time'][:], data.variables['radar_lon'][:])
# ax.plot(data.variables['radar_time'][:], data.variables['radar_giro'][:])
# ax.plot(data.variables['radar_time'][:], data.variables['radar_cog'][:])
# ax.plot(data.variables['radar_time'][:], 200*data.variables['radar_sog'][:])
# ax.plot(data.variables['radar_time'][:], data.variables['radar_theta'][:])
# ax.scatter(data.variables['radar_rad'][:], data.variables['radar_theta'][:])

plt.show()
