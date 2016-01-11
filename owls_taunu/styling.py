"""Plot styles for the tau+jet analysis.
"""

from six import string_types

from ROOT import TColor

# TODO: Pick one good series of divergent and sequential, and instead create
# series of different lenghts. Make sure divergent series can offer different
# lengths for left and right asymmetrically.

# (Line color, fill color, marker style, option (optional))
default_style = (1, 1, 8)
# Styles for plotting data (black) vs. MC (red)
default_black = (1, 1, 20)
default_red = (632, 1, 21)
# Styles for plotting data (black), MC (red), any (blue) in single drawable
# plots (same marker!)
default_black_thin = (1, 1, 8, 1)
default_blue_thin = (600, 1, 8, 1)
default_red_thin = (632, 1, 8, 1)
# Styles for plotting e.g. fit lines
line_black = (1, 1, 2)
line_black_thin = (1, 1, 1)
line_red = (632, 1, 2)
line_red_thin = (632, 1, 1)
line_dotted_red = (632, 3, 2)
line_dashed_grey = (12, 2, 2)
# Styles for plotting error bars only
# TODO: This is a huge hack.
bar_red = (632, 632, None, 2, 'E5')

# Divergent series 1-6 with 10 entries from http://colorbrewer2.org. The two
# lightest colours are disabled.
color_divergent = [
        # Series 1
        [
            "#543005",
            "#8c510a",
            "#bf812d",
            "#dfc27d",
            #"#f6e8c3",
            #"#c7eae5",
            "#80cdc1",
            "#35978f",
            "#01665e",
            "#003c30",
        ],
        # Series 2
        [
            "#8e0152",
            "#c51b7d",
            "#de77ae",
            "#f1b6da",
            #"#fde0ef",
            #"#e6f5d0",
            "#b8e186",
            "#7fbc41",
            "#4d9221",
            "#276419",
        ],
        # Series 3
        [
            "#40004b",
            "#762a83",
            "#9970ab",
            "#c2a5cf",
            #"#e7d4e8",
            #"#d9f0d3",
            "#a6dba0",
            "#5aae61",
            "#1b7837",
            "#00441b",
        ],
        # Series 4
        [
            "#7f3b08",
            "#b35806",
            "#e08214",
            "#fdb863",
            #"#fee0b6",
            #"#d8daeb",
            "#b2abd2",
            "#8073ac",
            "#542788",
            "#2d004b",
        ],
        # Series 5
        [
            "#67001f",
            "#b2182b",
            "#d6604d",
            "#f4a582",
            #"#fddbc7",
            #"#d1e5f0",
            "#92c5de",
            "#4393c3",
            "#2166ac",
            "#053061",
        ],
        # Series 6
        [
            "#a50026",
            "#d73027",
            "#f46d43",
            "#fdae61",
            #"#fee090",
            #"#e0f3f8",
            "#abd9e9",
            "#74add1",
            "#4575b4",
            "#313695",
        ],
]

color_sequential = [
        # Series 1
        [
            #"#f7fcfd",
            "#e5f5f9",
            "#ccece6",
            "#99d8c9",
            "#66c2a4",
            "#41ae76",
            "#238b45",
            "#006d2c",
            "#00441b",
        ],
        [
            #"#f7fcfd",
            "#e0ecf4",
            "#bfd3e6",
            "#9ebcda",
            "#8c96c6",
            "#8c6bb1",
            "#88419d",
            "#810f7c",
            "#4d004b",
        ],
        # TODO: ADD MORE!
]

marker_styles = [20, 21, 22, 23, 24, 25, 26, 32,]

def create_style(kind, series):
    """Create a list of styles (line color, fill color, marker style) from
    predefined sets.

    Args:
        kind: Kind of color scheme. Currently 'divergent' is the only
            supported kind.

        series: Sequential number representing the color scheme. Valid series
            for the different kinds are

            'divergent' - 1-6
            'sequential' - 1-2
    """
    if kind == 'divergent':
        if series < 1 or series > 6:
            raise RuntimeError('undefined style series {0} for kind {1}'. \
                    format(series, kind))
        return [(col, col, style)
                for col, style
                in zip(color_divergent[series-1], marker_styles)]
    if kind == 'sequential':
        if series < 1 or series > 2:
            raise RuntimeError('undefined style series {0} for kind {1}'. \
                    format(series, kind))
        return [(col, col, style)
                for col, style
                in zip(color_divergent[series-1], marker_styles)]
    else:
        raise RuntimeError('undefined style kind {0}'. \
                format(kind))

def create_divergent_style(series):
    """Create a list of styles (line color, fill color, marker style) from
    predefined sets.

    Args:
        series: Sequential number representing the color scheme. Valid series
            for the different kinds are
    """
    if series < 1 or series > 6:
        raise RuntimeError('undefined divergent style series {0}'. \
                format(series))
    l = [(col, col, style)
            for col, style
            in zip(color_divergent[series-1], marker_styles)]
    return (l[0:len(l)/2], l[len(l)/2:])

def pick_styles(styles, count):
    l = len(styles)
    if count is None:
        return styles
    elif count == 1:
        return styles[l/2:l/2+1]
    elif count == 2:
        return [styles[l/4], styles[3*l/4]]
    elif count <= l / 2:
        return styles[1::2]
    else:
        return styles


def create_sequential_style(series, line_width = None, count = None):
    """Create a list of styles (line color, fill color, marker style) from
    predefined sets.

    Args:
        series: Sequential number representing the color scheme. Valid series
            for the different kinds are
        count: Optional parameter to pick among the available styles for
            improved contrast
    """
    if series < 1 or series > 2:
        raise RuntimeError('undefined sequential style series {0}'. \
                format(series))
    if line_width is not None:
        # TODO: Optional line style
        styles = [(col, 1, line_width)
                  for col
                  in color_sequential[series-1]]

    else:
        styles = [(col, col, style)
                  for col, style
                  in zip(color_sequential[series-1], marker_styles)]
    return pick_styles(styles, count)
