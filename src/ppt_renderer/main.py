from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import parse_presentation_spec
from .renderers import ImageRenderer, Renderer, SlideRenderer, TextRenderer
from .schema import validate_payload


def generate_ppt(json_input: dict, output_path: str) -> None:
    normalized = validate_payload(json_input)
    spec = parse_presentation_spec(normalized)
    renderer = Renderer(slide_renderer=SlideRenderer(text_renderer=TextRenderer(), image_renderer=ImageRenderer()))
    renderer.render(spec, output_path)


def _resolve_relative_image_paths(payload: dict[str, Any], input_dir: Path) -> dict[str, Any]:
    slides = payload.get("slides", [])
    for slide in slides:
        for element in slide.get("elements", []):
            if element.get("type") != "image":
                continue
            raw_path = element.get("path")
            if not raw_path:
                continue
            candidate = Path(raw_path)
            if candidate.is_absolute():
                continue
            element["path"] = str((input_dir / candidate).resolve())
    return payload


def generate_ppt_from_file(input_json_path: str, output_path: str) -> None:
    path = Path(input_json_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    data = _resolve_relative_image_paths(data, path.parent)
    generate_ppt(data, output_path)
