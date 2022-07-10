from utility import *
from drawers import *
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np

data = nc.Dataset('4035.nc')  # имя файла с данными
bsktr = data.variables["bsktr"]

radar = radar_from_data(data)  # структура массивов numpy со всеми параметрами о радаре кроме самой bsktr

area = Area(2000, 2000, 500, 270)  # параметры прямоугольника исследования
resolution = 1000  # количество узлов в сетке по обеим осям (в данном файле максимально 4096)

time = 0
bsktr_cur = np.transpose(np.array(bsktr[time]))
map_res, vertex = make_area(bsktr_cur, resolution, resolution, area, radar.rad[-1])
print(vertex)

# отрисовываем поле внутри рамки
plt.subplot(111)
draw_map(map_res, vertex)

# отрисовываем бар
plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
cax = plt.axes([0.85, 0.1, 0.075, 0.8])
plt.colorbar(cax=cax)

plt.show()
