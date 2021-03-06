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


make_matrix()

