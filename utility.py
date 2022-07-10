from dataclasses import dataclass
import numpy as np


@dataclass
class Area:
    """
    структура исследуемого прямоугольника
    """
    width: float  # ширина прямоугольника
    height: float  # высота прямоугольника
    distance: float  # расстояние от радара до центра прямоугольника
    azimuth: float  # угол между 0 углом радара и направлением на центр прямоугольника


@dataclass
class Radar:
    """
    структура данных с радара
    """
    time: np.ndarray  # время с радара (с от 01.01.1970)
    latitude: np.ndarray  # широта радара (град)
    longitude: np.ndarray  # долгота радара (град)
    giro: np.ndarray  # данные с гирокомпаса (град)
    cog: np.ndarray  # курс относительно земли (град)
    sog: np.ndarray  # скорость относительно земпи (м/с)
    rad: np.ndarray  # сетка по радиусу (м)
    theta: np.ndarray  # сетка по углу (град)


def radar_from_data(data):
    # создание радара по данным
    return Radar(np.array(data.variables["radar_time"][:]),
                 np.array(data.variables["radar_lat"][:]),
                 np.array(data.variables["radar_lon"][:]),
                 np.array(data.variables["radar_giro"][:]),
                 np.array(data.variables["radar_cog"][:]),
                 np.array(data.variables["radar_sog"][:]),
                 np.array(data.variables["radar_rad"][:]),
                 np.array(data.variables["radar_theta"][:]))


def make_cart_map_rough(map: np.ndarray, rad_size, th_size):
    """
    представление данных с радара в декартовых координатах без интерполяции
    :param map: данные bsktr
    :param rad_size: число узлов в сетке по радиусу
    :param th_size: число узлов в сетке по углу
    :return: массив в коодинатах x, y
    """
    res = np.ndarray(shape=(2 * rad_size, 2 * rad_size), dtype=float)

    for x in range(-rad_size, rad_size):
        for y in range(-rad_size, rad_size):
            r = np.sqrt(x ** 2 + y ** 2)
            if r >= rad_size:
                res[x + rad_size, y + rad_size] = 0
            else:
                if x > 0 and y > 0:
                    res[x + rad_size, y + rad_size] = map[
                        int(r), int((np.abs(np.arctan(y / x)) + np.pi / 2) / 2 / np.pi * th_size)]
                elif x > 0 and y < 0:
                    res[x + rad_size, y + rad_size] = map[
                        int(r), int((np.abs(np.arctan(x / y))) / 2 / np.pi * th_size)]
                elif x < 0 and y < 0:
                    res[x + rad_size, y + rad_size] = map[
                        int(r), int((2 * np.pi - np.abs(np.arctan(x / y))) / 2 / np.pi * th_size)]
                elif x < 0 and y > 0:
                    res[x + rad_size, y + rad_size] = map[
                        int(r), int((np.pi + np.abs(np.arctan(x / y))) / 2 / np.pi * th_size)]
                elif x == 0 and y > 0:
                    res[x + rad_size, y + rad_size] = map[int(r), int(0.5 * th_size)]
                elif x == 0 and y < 0:
                    res[x + rad_size, y + rad_size] = map[int(r), 0]
                elif y == 0 and x > 0:
                    res[x + rad_size, y + rad_size] = map[int(r), int(0.25 * th_size)]
                elif y == 0 and x < 0:
                    res[x + rad_size, y + rad_size] = map[int(r), int(0.75 * th_size)]
                else:
                    res[x + rad_size, y + rad_size] = map[0, 0]

    return res


def make_cart_map_bilinear(map: np.ndarray, rad_size, th_size):
    """
    представление данных с радара в декартовых координатах с билинейной интерполяцией
    :param map: данные bsktr
    :param rad_size: число узлов в сетке по радиусу
    :param th_size: число узлов в сетке по углу
    :return: массив в коодинатах x, y
    """
    res = np.ndarray(shape=(2 * rad_size, 2 * rad_size), dtype=float)

    for x in range(-rad_size, rad_size):
        for y in range(-rad_size, rad_size):
            r = np.sqrt(x ** 2 + y ** 2)
            if r >= rad_size:
                res[x + rad_size, y + rad_size] = 0
            else:
                r /= rad_size
                r *= map.shape[0]
                th = 0
                if x > 0 and y > 0:
                    th = (np.abs(np.arctan(y / x)) + np.pi / 2) / 2 / np.pi * th_size
                elif x > 0 and y < 0:
                    th = (np.abs(np.arctan(x / y))) / 2 / np.pi * th_size
                elif x < 0 and y < 0:
                    th = (2 * np.pi - np.abs(np.arctan(x / y))) / 2 / np.pi * th_size
                elif x < 0 and y > 0:
                    th = (np.pi + np.abs(np.arctan(x / y))) / 2 / np.pi * th_size
                elif x == 0 and y > 0:
                    th = 0.5 * th_size
                elif x == 0 and y < 0:
                    th = 0
                elif y == 0 and x > 0:
                    th = 0.25 * th_size
                elif y == 0 and x < 0:
                    th = 0.75 * th_size
                else:
                    r = 0
                th_div = int(th)
                th_mod = th - th_div
                r_div = int(r)
                r_mod = r - r_div

                if r_div == map.shape[0] - 1:
                    if th_div == map.shape[1] - 1:
                        res[x + rad_size, y + rad_size] = map[r_div, th_div]
                    else:
                        res[x + rad_size, y + rad_size] = (1 - th_mod) * map[r_div, th_div] + th_mod * map[
                            r_div, th_div + 1]
                elif th_div == map.shape[1] - 1:
                    res[x + rad_size, y + rad_size] = (1 - r_mod) * map[r_div, th_div] + r_mod * map[
                        r_div + 1, th_div]
                else:
                    res[x + rad_size, y + rad_size] = (1 - r_mod) * (1 - th_mod) * map[r_div, th_div] + \
                                                      (1 - r_mod) * th_mod * map[r_div, th_div + 1] + \
                                                      r_mod * (1 - th_mod) * map[r_div + 1, th_div] + \
                                                      r_mod * th_mod * map[r_div + 1, th_div + 1]
        if x % 100 == 0:
            print(x)

    return res


def make_area(map: np.ndarray, rad_size, th_size, area: Area, rad_lim):
    """
    представление данных с радара в декартовых координатах без интерполяции
    :param map: данные bsktr
    :param rad_size: число узлов в сетке по радиусу
    :param th_size: число узлов в сетке по углу
    :param area: структура с данными об вырезаемом прямоугольнике
    :param rad_lim: предел по радиусу
    :return: массив в координатах x, y
    """
    az = ((area.azimuth / 180) - 0.5) * np.pi
    r_sin = area.distance * np.sin(az)
    r_cos = area.distance * np.cos(az)
    x_left = round((r_sin - 0.5 * area.width) / rad_lim * rad_size)
    x_right = round((r_sin + 0.5 * area.width) / rad_lim * rad_size) + 1
    y_bot = round((r_cos - 0.5 * area.height) / rad_lim * rad_size)
    y_top = round((r_cos + 0.5 * area.height) / rad_lim * rad_size) + 1

    res = np.ndarray(shape=(x_right - x_left, y_top - y_bot), dtype=float)

    for x in range(x_left, x_right):
        for y in range(y_bot, y_top):
            r = np.sqrt(x ** 2 + y ** 2)
            if r >= rad_size:
                res[-x + x_left, y - y_bot] = 0
            else:
                r /= rad_size
                r *= map.shape[0]
                th = 0
                if x > 0 and y > 0:
                    th = (np.arctan(x / y) / 2 / np.pi + 0.25) * th_size
                elif x > 0 and y < 0:
                    th = (np.abs(np.arctan(y / x)) / 2 / np.pi + 0.5) * th_size
                elif x < 0 and y < 0:
                    th = (0.75 + np.abs(np.arctan(x / y)) / 2 / np.pi) * th_size
                elif x < 0 and y > 0:
                    th = (0.25 - np.abs(np.arctan(x / y)) / 2 / np.pi) * th_size
                elif x == 0 and y > 0:
                    th = 0.25 * th_size
                elif x == 0 and y < 0:
                    th = 0.75 * th_size
                elif y == 0 and x > 0:
                    th = 0.5 * th_size
                elif y == 0 and x < 0:
                    th = 0
                else:
                    r = 0
                th_div = int(th)
                th_mod = th - th_div
                r_div = int(r)
                r_mod = r - r_div

                if r_div >= map.shape[0] - 1 or r_div <= 0:
                    if th_div >= map.shape[1] - 1 or th_div <= 0:
                        res[-x + x_left, y - y_bot] = map[r_div, th_div]
                    else:
                        res[-x + x_left, y - y_bot] = (1 - th_mod) * map[r_div, th_div] + th_mod * map[
                            r_div, th_div + 1]
                elif th_div >= map.shape[1] - 1 or th_div <= 0:
                    res[-x + x_left, y - y_bot] = (1 - r_mod) * map[r_div, th_div] + r_mod * map[
                        r_div + 1, th_div]
                else:
                    res[-x + x_left, y - y_bot] = (1 - r_mod) * (1 - th_mod) * map[r_div, th_div] + \
                                                  (1 - r_mod) * th_mod * map[r_div, th_div + 1] + \
                                                  r_mod * (1 - th_mod) * map[r_div + 1, th_div] + \
                                                  r_mod * th_mod * map[r_div + 1, th_div + 1]

        if ((x - x_left) / (x_right - x_left) * 100) % 25 == 0:
            print((x - x_left) / (x_right - x_left) * 100)

    return res, np.array(
        [r_cos - 0.5 * area.width, r_cos + 0.5 * area.width,
         r_sin + 0.5 * (np.cos(area.azimuth / 180 * np.pi) - 1) * area.height, r_sin + 0.5 * (np.cos(area.azimuth/ 180 * np.pi) + 1) * area.height])
