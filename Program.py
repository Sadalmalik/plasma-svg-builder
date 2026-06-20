# python
# import css_parser
from SvgBuilder import *


def main():
    print("test")
    write_svg("output/image-new.svg")


def write_svg(name):
    header = XmlHeader()
    content = Svg(width=500, height=500, children=[
    #   GuiBuilder(30, 30).build_tiled_box()

        Group("rounded", x=20, y=-20, children=[bild_corner_rounded(30, 20)]),
        Group("bevel",   x=70, y=-20, children=[bild_corner_bevel  (30, 20)]),
        Group("bezier",  x=20, y=-70, children=[bild_corner_bezier (30, 20, 0.2)]),
        Group("bezier",  x=70, y=-70, children=[bild_corner_bezier (30, 20, 0.8)]),
        build_buttons(30, [0, 5, 10, 15], False),

    #     Group("MyGroup", transform="rotate(45)", children=[
    #         Rect("central", width=50, height=50, fill="#DD8822", transform="translate(50,50)"),
    #         Rect("left", width=20, height=50, fill="black", transform="translate(10,50)"),
    #     ], **{
    #         "transform-origin": "center"
    #     }),
    ])

    text = str(header) + '\n' + str(content)
    with open(name, "w") as out:
        out.write(text)


class Style:
    def __init__(self, margin: list[int], padding: list[int], border_width=0):
        self.margin = margin
        self.padding = padding
        self.border_width = border_width


def normalize_sides_arguments(margin: list[int|float]):
    pass


def normalize_corner_arguments(margin: list[int|float] | int | float):
    if isinstance(margin, int) or isinstance(margin, float):
        return [margin, margin, margin, margin]
    elif len(margin) == 1:
        return [margin[0], margin[0], margin[0], margin[0]]
    elif len(margin) == 2:
        return [margin[0], margin[1], margin[0], margin[1]]
    elif len(margin) == 3:
        return [margin[0], margin[1], margin[2], margin[1]]
    return margin


def build_buttons(size, radius, is_bevel=False):
    radius = normalize_corner_arguments(radius)
    return Group(
        "buttons",
        children=[
            build_tiled_box("normal",  size=size, border_radius=radius, is_bevel=is_bevel, x=1*size, y= 1*size),
            build_tiled_box("hover",   size=size, border_radius=radius, is_bevel=is_bevel, x= 5*size, y= 1*size),
            build_tiled_box("pressed", size=size, border_radius=radius, is_bevel=is_bevel, x= 1*size, y= 5*size),
            build_tiled_box("focused", size=size, border_radius=radius, is_bevel=is_bevel, x= 5*size, y= 5*size),
        ]
    )


def build_tiled_box(name='', size=0, border_radius=0,  is_bevel=False, **kwargs):
    prefix = '' if name == '' else name+'-'
    max_radius = max(border_radius)
    half_size = max_radius / 2
    build_corner = bild_corner_bevel if is_bevel else bild_corner_rounded
    steps = [0, max_radius, max_radius+size]
    return Group(
        f"group:{name}" if name != '' else "group",
        **kwargs, # **{"inkscape:label": "#test"},
        children=[
            Group(id=f"{prefix}topleft",     x=steps[0], y=steps[0], children=[build_corner(max_radius, border_radius[0])]),
            Group(id=f"{prefix}top",         x=steps[1], y=steps[0], children=[Rect(width=size, height=max_radius)]),
            Group(id=f"{prefix}topright",    x=steps[2], y=steps[0], children=[build_corner(max_radius, border_radius[1])], rotate=f"90 {half_size} {half_size}"),

            Group(id=f"{prefix}left",        x=steps[0], y=steps[1], children=[Rect(width=max_radius, height=size)]),
            Group(id=f"{prefix}center",      x=steps[1], y=steps[1], children=[Rect(width=size, height=size)]),
            Group(id=f"{prefix}right",       x=steps[2], y=steps[1], children=[Rect(width=max_radius, height=size)]),

            Group(id=f"{prefix}bottomleft",  x=steps[0], y=steps[2], children=[build_corner(max_radius, border_radius[3])], rotate=f"270 {half_size} {half_size}"),
            Group(id=f"{prefix}bottom",      x=steps[1], y=steps[2], children=[Rect(width=size, height=max_radius)]),
            Group(id=f"{prefix}bottomright", x=steps[2], y=steps[2], children=[build_corner(max_radius, border_radius[2])], rotate=f"180 {half_size} {half_size}"),
        ])


def bild_corner_rounded(size: float, radius: float, **kwargs):
    commands = [
        f"M {size} {size}",
        f"L {0} {size}",
        f"L {0} {radius}",
        f"A {radius} {radius} 0 0 1 {radius} {0}",
        f"L {size} {0}",
        f"L {size} {size}",
    ]
    return Path(width=size, height=size, **kwargs, d=" ".join(commands))


def bild_corner_bevel(size, radius, **kwargs):
    commands = [
        f"M {size} {size}",
        f"L {0} {size}",
        f"L {0} {radius}",
        f"L {radius} {0}",
        f"L {size} {0}",
        f"L {size} {size}",
    ]
    return Path(width=size, height=size, **kwargs, d=" ".join(commands))


def bild_corner_bezier(size, radius, smooth=0.1, **kwargs):
    commands = [
        f"M {size} {size}",
        f"L {0} {size}",
        f"L {0} {radius}",
        f"C {0} {radius * (1-smooth)}",
          f"{radius * (1-smooth)} {0}",
          f"{radius} {0}",
        f"L {size} {0}",
        f"L {size} {size}",
    ]
    return Path(width=size, height=size, **kwargs, d=" ".join(commands))


if __name__=="__main__":
    main()
