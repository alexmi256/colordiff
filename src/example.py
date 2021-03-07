from colormath.color_objects import LabColor, sRGBColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color
from colored.hex import _xterm_colors
import numpy as np
import random
from rich.console import Console
from rich.table import Table
from rich.text import Text


# TODO: Instead of console tables, make a heatmap graphic
# TODO: Instead of console tables, try to make some interactive web graph


def print_matrix(hex_colors, distance_matrix, title='Color Similarity Matrix'):
    """
    Print out a table for the given
    :param hex_colors: A list of hex color strings
    :param distance_matrix: A distance matrix of the hex colors
    :param title: Title of the chart
    :return:
    """

    # Print out a nice table of the similarity matrix
    console = Console(width=420, color_system='truecolor')
    table = Table(title=title, show_header=True)
    table.add_column('')
    for color in hex_colors:
        table.add_column(Text(color[1:], style=f'bold {color}'))

    for i, row in enumerate(distance_matrix):
        header = Text(hex_colors[i], style=f'bold {hex_colors[i]}')
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


def make_matrix(size=15):
    """
    Make a distance matrix of random terminal colors
    :return:
    """
    # Choose some random color
    all_colors_hex = list(_xterm_colors.values())
    chosen_colors_hex = random.sample(all_colors_hex, size)
    chosen_colors_rgb = [sRGBColor.new_from_rgb_hex(x) for x in chosen_colors_hex]
    chosen_colors_lab = [convert_color(x, LabColor) for x in chosen_colors_rgb]

    # Generate a similarity matrix of all colors
    distance_matrix = np.zeros(shape=(size, size), dtype=float)
    for i, color_1 in enumerate(chosen_colors_lab):
        for j, color_2 in enumerate(chosen_colors_lab):
            distance_matrix[i, j] = delta_e_cie2000(color_1, color_2)

    print_matrix(chosen_colors_hex, distance_matrix)

    return chosen_colors_hex, distance_matrix


def print_clusters(colors, clusters, distance_matrix):
    """
    Prints out a distance matrix for each calculated cluster
    :param colors:
    :param clusters:
    :param distance_matrix:
    :return:
    """
    print(f'There were {len(set(clusters))} clusters found')
    # We need to group the colors and create a new matrix for each cluster
    divided_clusters = {k: {'colors': []} for k in set(clusters)}

    # Add the colors to each cluster
    for color, cluster_number in zip(colors, clusters):
        divided_clusters[cluster_number]['colors'].append(color)

    for cluster in divided_clusters.values():
        cluster['matrix'] = np.zeros(shape=(len(cluster['colors']), len(cluster['colors'])), dtype=float)
        # Create a sub matrix for each color
        for i, color_1 in enumerate(cluster['colors']):
            for j, color_2 in enumerate(cluster['colors']):
                cluster['matrix'][i, j] = distance_matrix[colors.index(color_1), colors.index(color_2)]

    for i, cluster in divided_clusters.items():
        print_matrix(cluster['colors'], cluster['matrix'], title=f'Cluster #{i + 1}')

