from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class BoxModel(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)


class TextStyleModel(BaseModel):
    font_name: str = "Arial"
    font_size_pt: float = Field(default=18.0, gt=0)
    bold: bool = False
    italic: bool = False
    color_hex: str = Field(default="000000", pattern=r"^[0-9A-Fa-f]{6}$")
    align: Literal["left", "center", "right", "justify"] = "left"
    valign: Literal["top", "middle", "bottom"] = "top"
    auto_fit_font: bool = False
    min_font_size_pt: float = Field(default=10.0, gt=0)
    max_font_size_pt: float = Field(default=48.0, gt=0)
    wrap: bool = True


class TextElementModel(BaseModel):
    type: Literal["text"]
    box: BoxModel
    text: str
    style: TextStyleModel = Field(default_factory=TextStyleModel)


class ImageElementModel(BaseModel):
    type: Literal["image"]
    box: BoxModel
    path: str
    crop_mode: Literal["contain", "cover", "fit"] = "contain"


class SlideModel(BaseModel):
    elements: list[TextElementModel | ImageElementModel]


class SlideSizeModel(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)


class PresentationModel(BaseModel):
    slide_size: SlideSizeModel
    slides: list[SlideModel]


def validate_payload(payload: dict) -> dict:
    try:
        return PresentationModel.model_validate(payload).model_dump()
    except ValidationError as exc:
        raise ValueError(f"Invalid payload: {exc}") from exc
