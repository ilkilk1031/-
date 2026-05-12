import json
from pathlib import Path

from ppt_renderer.main import _resolve_relative_image_paths


def test_resolve_relative_image_paths_from_input_file_dir(tmp_path: Path) -> None:
    assets = tmp_path / "assets"
    assets.mkdir()
    img = assets / "sample.png"
    img.write_bytes(b"x")

    payload = {
        "slides": [
            {
                "elements": [
                    {"type": "image", "path": "assets/sample.png", "box": {"x": 0, "y": 0, "width": 1, "height": 1}},
                    {"type": "text", "text": "hello", "box": {"x": 0, "y": 0, "width": 1, "height": 1}},
                ]
            }
        ]
    }

    result = _resolve_relative_image_paths(payload, tmp_path)
    assert Path(result["slides"][0]["elements"][0]["path"]).is_absolute()
    assert result["slides"][0]["elements"][0]["path"].endswith("assets/sample.png")
