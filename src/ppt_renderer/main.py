from __future__ import annotations

import json
from pathlib import Path

from .models import parse_presentation_spec
from .renderers import ImageRenderer, Renderer, SlideRenderer, TextRenderer


def generate_ppt(json_input: dict, output_path: str) -> None:
    spec = parse_presentation_spec(json_input)
    renderer = Renderer(slide_renderer=SlideRenderer(text_renderer=TextRenderer(), image_renderer=ImageRenderer()))
    renderer.render(spec, output_path)


def generate_ppt_from_file(input_json_path: str, output_path: str) -> None:
    path = Path(input_json_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    generate_ppt(data, output_path)
