from colormath.color_objects import LabColor, sRGBColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color
from colored.hex import _xterm_colors
import matplotlib.pyplot as plt
import numpy as np
import random
from rich.console import Console
from rich.table import Table
from rich.text import Text
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import DBSCAN

NUMBER_OF_COLORS = 15


def make_matrix():
    """
    Print out and return a 2D numpy array consisting of a distance matrix
    :return:
    """
    # Choose some random color
    all_colors_hex = list(_xterm_colors.values())
    chosen_colors_hex = random.sample(all_colors_hex, NUMBER_OF_COLORS)
    chosen_colors_rgb = [sRGBColor.new_from_rgb_hex(x) for x in chosen_colors_hex]
    chosen_colors_lab = [convert_color(x, LabColor) for x in chosen_colors_rgb]

    # Generate a similarity matrix of all colors
    distance_matrix = np.zeros(shape=(NUMBER_OF_COLORS, NUMBER_OF_COLORS), dtype=float)
    for i, color_1 in enumerate(chosen_colors_lab):
        for j, color_2 in enumerate(chosen_colors_lab):
            distance_matrix[i, j] = delta_e_cie2000(color_1, color_2)

    # Print out a nice table of the similarity matrix
    console = Console(width=420, color_system='truecolor')
    table = Table(title='Color Similarity Matrix', show_header=True)
    table.add_column('')
    for color in chosen_colors_hex:
        table.add_column(Text(color[1:], style=f'bold {color}'))

    for i, row in enumerate(distance_matrix):
        header = Text(chosen_colors_hex[i], style= f'bold {chosen_colors_hex[i]}')
        colored_row = [header]
        for column_value in row:
            # Here is something I completely made up based on personal observation that won't work for anything else
            if column_value <= 0:
                # lime
                color_value = '#00ff00'
            elif column_value <= 2:
                # green
                color_value = '#008000'
            elif column_value <= 10:
                # green yellow
                color_value = '#afff00'
            elif column_value <= 27:
                # orange1
                color_value = '#ffaf00'
            elif column_value <= 49:
                # yellow
                color_value = '#ffff00'
            else:
                # red
                color_value = '#ff0000'
            colored_row.append(Text(f'{column_value:.2f}', style=color_value))
        table.add_row(*colored_row)

    console.print(table)
    return distance_matrix

# Try out DBScan
distance_matrix = make_matrix()
distances = pairwise_distances(distance_matrix, metric="precomputed")

# Compute DBSCAN
# The results are pretty bad
db = DBSCAN(eps=20, metric="precomputed", min_samples=1).fit(distances)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)

# #############################################################################
# Plot result

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = labels == k

    xy = distances[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], "o", markerfacecolor=tuple(col), markeredgecolor="k", markersize=14)

    xy = distances[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], "o", markerfacecolor=tuple(col), markeredgecolor="k", markersize=6)

plt.title("Estimated number of clusters: %d" % n_clusters_)
plt.show()

