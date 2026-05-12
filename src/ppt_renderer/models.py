from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

CropMode = Literal["contain", "cover", "fit"]


@dataclass(frozen=True)
class SlideSize:
    width: int
    height: int


@dataclass(frozen=True)
class TextStyle:
    font_name: str = "Arial"
    font_size_pt: float = 18.0
    bold: bool = False
    italic: bool = False
    color_hex: str = "000000"
    align: Literal["left", "center", "right", "justify"] = "left"
    valign: Literal["top", "middle", "bottom"] = "top"
    auto_fit_font: bool = False
    min_font_size_pt: float = 10.0
    max_font_size_pt: float = 48.0
    wrap: bool = True


@dataclass(frozen=True)
class Box:
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class TextElement:
    type: Literal["text"]
    box: Box
    text: str
    style: TextStyle = field(default_factory=TextStyle)


@dataclass(frozen=True)
class ImageElement:
    type: Literal["image"]
    box: Box
    path: str
    crop_mode: CropMode = "contain"


Element = TextElement | ImageElement


@dataclass(frozen=True)
class SlideSpec:
    elements: tuple[Element, ...]


@dataclass(frozen=True)
class PresentationSpec:
    slide_size: SlideSize
    slides: tuple[SlideSpec, ...]


def parse_presentation_spec(data: dict[str, Any]) -> PresentationSpec:
    size = data["slide_size"]
    slide_size = SlideSize(width=int(size["width"]), height=int(size["height"]))

    slides: list[SlideSpec] = []
    for slide_data in data["slides"]:
        elements: list[Element] = []
        for elem in slide_data["elements"]:
            b = elem["box"]
            box = Box(x=int(b["x"]), y=int(b["y"]), width=int(b["width"]), height=int(b["height"]))
            if elem["type"] == "text":
                style_data = elem.get("style", {})
                style = TextStyle(
                    font_name=style_data.get("font_name", "Arial"),
                    font_size_pt=float(style_data.get("font_size_pt", 18.0)),
                    bold=bool(style_data.get("bold", False)),
                    italic=bool(style_data.get("italic", False)),
                    color_hex=style_data.get("color_hex", "000000"),
                    align=style_data.get("align", "left"),
                    valign=style_data.get("valign", "top"),
                    auto_fit_font=bool(style_data.get("auto_fit_font", False)),
                    min_font_size_pt=float(style_data.get("min_font_size_pt", 10.0)),
                    max_font_size_pt=float(style_data.get("max_font_size_pt", 48.0)),
                    wrap=bool(style_data.get("wrap", True)),
                )
                elements.append(TextElement(type="text", box=box, text=str(elem["text"]), style=style))
            elif elem["type"] == "image":
                elements.append(
                    ImageElement(
                        type="image",
                        box=box,
                        path=str(elem["path"]),
                        crop_mode=elem.get("crop_mode", "contain"),
                    )
                )
            else:
                raise ValueError(f"Unsupported element type: {elem['type']}")
        slides.append(SlideSpec(elements=tuple(elements)))

    return PresentationSpec(slide_size=slide_size, slides=tuple(slides))
