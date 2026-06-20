# python

def _convert_transform(kwargs):
    x = kwargs.get("x", 0)
    y = kwargs.get("y", 0)
    rotate = kwargs.get("rotate", None)
    transform = ""
    if x != 0 or y != 0:
        transform += f" translate({x}, {y})"
        if "x" in kwargs: del kwargs["x"]
        if "y" in kwargs: del kwargs["y"]
    if rotate is not None:
        transform += f" rotate({rotate})"
        del kwargs["rotate"]
    transform = transform.strip()
    if len(transform) > 0:
        kwargs["transform"] = transform


class XmlTag:
    def __init__(self, name: str = 'tag', modifier: str = '', force_oneline=False, *args, **kwargs):
        self.name = name
        self.modifier = modifier
        self.force_oneline = force_oneline
        self.properties = kwargs or {}
        self.children: list[XmlTag] = []
        if "children" in self.properties:
            self.children.extend(self.properties.pop("children"))
    
    def add_prop(self, key: str, value):
        self.properties[key] = value
    
    def add_child(self, child: XmlTag):
        self.children.append(child)
        self.force_oneline = False

    def __render(self, lines: list, indent: int):
        ind_body = " " * indent
        ind_prop = " " * (indent + 3)
        lines.append(ind_body)
        lines.append("<")
        lines.append(self.modifier)
        lines.append(self.name)
        for key, value in self.properties.items():
            if self.force_oneline:
                lines.append(' ')
            else:
                lines.append("\n")
                lines.append(ind_prop)
            lines.append(str(key))
            lines.append("=\"")
            lines.append(str(value))
            lines.append("\"")
        if len(self.children) > 0:
            lines.append(">")
            for child in self.children:
                if child is None:
                    continue
                lines.append("\n")
                child.__render(lines, indent+2)
            lines.append("\n")
            lines.append(ind_body)
            lines.append("</")
            lines.append(self.name)
            lines.append(">")
        elif len(self.modifier) > 0:
            lines.append(self.modifier)
            lines.append(">")
        else:
            lines.append(" />")

    def __str__(self):
        lines = []
        self.__render(lines, 0)
        return ''.join(lines)


class XmlHeader(XmlTag):
    def __init__(self):
        super().__init__('xml', '?',
            force_oneline=True,
            version = "1.0",
            encoding = "UTF-8",
            standalone = "no")


class Svg(XmlTag):
    def __init__(self, **kwargs):
        super().__init__('svg',
            baseProfile="full",
            **{
                "xmlns": "http://www.w3.org/2000/svg",
                "xmlns:xlink": "http://www.w3.org/1999/xlink",
                "xmlns:ev": "http://www.w3.org/2001/xml-events",
            },
            **kwargs)


class Group(XmlTag):
    def __init__(self, id, children, **kwargs):
        _convert_transform(kwargs)
        super().__init__('g', id=id, children=children, **kwargs)


class Rect(XmlTag):
    def __init__(self, **kwargs):
        _convert_transform(kwargs)
        super().__init__('rect', **kwargs)


class Circle(XmlTag):
    def __init__(self, **kwargs):
        _convert_transform(kwargs)
        super().__init__('circle', **kwargs)


class Line(XmlTag):
    def __init__(self, **kwargs):
        _convert_transform(kwargs)
        super().__init__('line', **kwargs)


class Path(XmlTag):
    def __init__(self, **kwargs):
        _convert_transform(kwargs)
        super().__init__('path', **kwargs)