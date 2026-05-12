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


def test_resolve_relative_image_paths_keeps_existing_repo_relative_path(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    examples = repo / "examples"
    examples.mkdir(parents=True)
    (examples / "sample_input.json").write_text("{}", encoding="utf-8")
    image = examples / "assets" / "sample.png"
    image.parent.mkdir(parents=True)
    image.write_bytes(b"x")

    payload = {
        "slides": [
            {
                "elements": [
                    {"type": "image", "path": "examples/assets/sample.png", "box": {"x": 0, "y": 0, "width": 1, "height": 1}}
                ]
            }
        ]
    }

    monkeypatch.chdir(repo)
    result = _resolve_relative_image_paths(payload, examples)
    assert result["slides"][0]["elements"][0]["path"] == str(image.resolve())
