import matplotlib.pyplot as plt


def draw_map(radar_map, vertex):
    return plt.imshow(radar_map, cmap='Blues', origin="lower", extent=vertex)
