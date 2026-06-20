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
        build_buttons(
            size=20,
            radius=[5, 5, 5, 5],
            margin=[8, 4, 6, 4],
            is_bevel=True),

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


def normalize_arguments(corners: list[int | float] | int | float):
    # order | sides    | corners
    #  0    |  top     | top-left
    #  1    |  right   | top-right
    #  2    |  bottom  | bottom-right
    #  3    |  left    | bottom-left
    if isinstance(corners, int) or isinstance(corners, float):
        return [corners, corners, corners, corners]
    elif len(corners) == 1:
        return [corners[0], corners[0], corners[0], corners[0]]
    elif len(corners) == 2:
        return [corners[0], corners[1], corners[0], corners[1]]
    elif len(corners) == 3:
        return [corners[0], corners[1], corners[2], corners[1]]
    return corners


def build_buttons(size, radius, margin, is_bevel=False):
    radius = normalize_arguments(radius)
    margin = normalize_arguments(margin)
    common = {
        "size": size,
        "radius": radius,
        "is_bevel": is_bevel,
        "margin": margin,
    }
    return Group(
        "buttons",
        children=[
            build_tiled_box("normal",  x= 1*size, y= 1*size, **common),
            build_tiled_box("hover",   x= 5*size, y= 1*size, **common),
            build_tiled_box("pressed", x= 1*size, y= 5*size, **common),
            build_tiled_box("focused", x= 5*size, y= 5*size, **common),
        ]
    )


def build_tiled_box(
        name='',
        size=0,
        radius: list[int | float] | int | float = 0,
        is_bevel=False,
        margin: list[int | float] | int | float | None = None,
        **kwargs):
    radius = normalize_arguments(radius)
    margin = normalize_arguments(margin)
    prefix = '' if name == '' else name+'-'
    max_radius = max(radius)
    half_size = max_radius / 2
    build_corner = bild_corner_bevel if is_bevel else bild_corner_rounded
    steps = [0, max_radius, max_radius+size]
    margin = normalize_arguments(margin) if margin is not None else None

    box = Group(
        f"group:{name}" if name != '' else "group",
        **kwargs,
        # **{"inkscape:label": "#test"},
        children=[]
    )

    # top row
    box.add_child(Group(id=f"{prefix}topleft",     x=steps[0], y=steps[0], children=[build_corner(max_radius, radius[0])]))
    box.add_child(Group(id=f"{prefix}top",         x=steps[1], y=steps[0], children=[Rect(width=size, height=max_radius)]))
    box.add_child(Group(id=f"{prefix}topright",    x=steps[2], y=steps[0], children=[build_corner(max_radius, radius[1])], rotate=f"90 {half_size} {half_size}"))

    #middle row
    box.add_child(Group(id=f"{prefix}left",        x=steps[0], y=steps[1], children=[Rect(width=max_radius, height=size)]))
    box.add_child(Group(id=f"{prefix}center",      x=steps[1], y=steps[1], children=[Rect(width=size, height=size)]))
    box.add_child(Group(id=f"{prefix}right",       x=steps[2], y=steps[1], children=[Rect(width=max_radius, height=size)]))

    # bottom row
    box.add_child(Group(id=f"{prefix}bottomleft",  x=steps[0], y=steps[2], children=[build_corner(max_radius, radius[3])], rotate=f"270 {half_size} {half_size}"))
    box.add_child(Group(id=f"{prefix}bottom",      x=steps[1], y=steps[2], children=[Rect(width=size, height=max_radius)]))
    box.add_child(Group(id=f"{prefix}bottomright", x=steps[2], y=steps[2], children=[build_corner(max_radius, radius[2])], rotate=f"180 {half_size} {half_size}"))

    if margin is not None:
        small = max(2, size * 0.1)
        offset = (size - small) / 2
        box.add_child(Rect(id=f"{prefix}hint-top-margin",
                           x=steps[1] + offset, y=steps[0],
                           width=small, height=margin[0],
                           fill="purple"))
        box.add_child(Rect(id=f"{prefix}hint-right-margin",
                           x=steps[2]+max_radius-margin[1], y=steps[1] + offset,
                           width=margin[1], height=small,
                           fill="purple"))
        box.add_child(Rect(id=f"{prefix}hint-bottom-margin",
                           x=steps[1] + offset, y=steps[2]+max_radius-margin[2],
                           width=small, height=margin[2],
                           fill="purple"))
        box.add_child(Rect(id=f"{prefix}hint-left-margin",
                           x=steps[0], y=steps[1] + offset,
                           width=margin[3], height=small,
                           fill="purple"))

    return box


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
