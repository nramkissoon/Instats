from colorsys import rgb_to_hls
from math import sqrt


def get_average_shades(color_dict, pixel_list):
    ret_dict = {}
    for color in color_dict:
        avg_shade = average_shade(color_dict[color])
        if avg_shade:  # some colors are not present in an image so the avg_shade is None
            ret_dict[color] = {}
            ret_dict[color] = {'RGB': avg_shade, 'HEX': '#%02x%02x%02x' % avg_shade,
                               '%': round(len(color_dict[color]) / len(pixel_list), 4)}
    return ret_dict


def average_shade(pixel_list):
    if len(pixel_list) == 0:
        return None
    r, g, b = 0, 0, 0
    for pixel in pixel_list:
        r += pixel[0]
        g += pixel[1]
        b += pixel[2]
    return round(r / len(pixel_list)), round(g / len(pixel_list)), round(b / len(pixel_list))


def rgb_to_hsl(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0  # normalize rgb values
    h, l, s = rgb_to_hls(r, g, b)
    return h * 360.0, s, l


def color_classifier(tup):
    r, g, b = tup
    h, s, l = rgb_to_hsl(r, g, b)
    if s >= .15:
        if 0 <= h < 40:
            return 'orange'
        elif 40 <= h < 80:
            return 'yellow'
        elif 80 <= h < 120:
            return 'green'
        elif 120 <= h < 160:
            return 'turquois'
        elif 160 <= h < 200:
            return 'cyan'
        elif 200 <= h < 240:
            return 'blue'
        elif 240 <= h < 280:
            return 'violet'
        elif 280 <= h < 320:
            return 'magenta'
        elif 320 <= h <= 360:
            return 'red'
    else:
        grey_cutoffs = [0.0, .25, .50, .75, 1.0]
        distances = []
        for val in grey_cutoffs:
            distances.append(abs(l - val))
        closest = grey_cutoffs[distances.index(min(distances))]
        if closest == 0.0:
            return "black"
        elif closest == .25:
            return "dark grey"
        elif closest == .50:
            return "grey"
        elif closest == .75:
            return "light grey"
        elif closest == 1.0:
            return "white"


def sort_colors(pixel_list):
    color_dict = {'red': [], 'orange': [], 'yellow': [],
                  'green': [], 'turquois': [], 'cyan': [],
                  'magenta': [], 'blue': [], 'violet': [],
                  'black': [], 'dark grey': [], 'grey': [],
                  'light grey': [], 'white': []}
    for pixel in pixel_list:
        color = color_classifier(pixel)
        color_dict[color].append(pixel)
    return color_dict


def color_difference(col1, col2):
    sum_of_sq = 0
    for i in range(3):
        sum_of_sq += (col1[i] - col2[i]) ** 2
    return sqrt(sum_of_sq) / (sqrt(3 * (255 ** 2)))
