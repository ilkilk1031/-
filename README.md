# Deterministic PPT Rendering Engine

Deterministic JSON-to-PPTX renderer package with Python API, CLI, and FastAPI deployment.

## Quick Start

```bash
pip install -e .
python examples/create_sample_asset.py
# If `ppt-renderer` is not found, use the module form below.
ppt-renderer --input examples/sample_input.json --output output/sample_deck.pptx
python -m ppt_renderer.cli --input examples/sample_input.json --output output/sample_deck.pptx
```

## Project Structure

```text
src/ppt_renderer/
  __init__.py
  main.py
  models.py
  renderers.py
  schema.py
  cli.py
  api.py
examples/
tests/
Dockerfile
pyproject.toml
```

## Usage

### Python API
```python
from ppt_renderer import generate_ppt_from_file

generate_ppt_from_file("examples/sample_input.json", "output/sample_deck.pptx")
```

### CLI
```bash
ppt-renderer --input examples/sample_input.json --output output/sample_deck.pptx
```


### Desktop UI
```bash
ppt-renderer-ui
```

Use the UI to add slides, set input/output/reference images, enter prompts, and export PPT.


### FastAPI (local)
```bash
uvicorn ppt_renderer.api:app --host 0.0.0.0 --port 8000
```

### CLI (PATH troubleshooting on Windows)
If you see `ppt-renderer: command not found` after installation, your user Scripts path is not on `PATH`.

Use either option:

1. Run without PATH setup:
```bash
python -m ppt_renderer.cli --input examples/sample_input.json --output output/sample_deck.pptx
```

2. Add this folder to Windows PATH, then reopen terminal:
```text
C:\Users\<YOUR_USER>\AppData\Roaming\Python\Python3XX\Scripts
```
Replace `Python3XX` with your installed version (for example `Python314`).


### FastAPI (Docker)
```bash
docker compose up --build
```

`POST /generate-ppt` with JSON payload and get `.pptx` response.

## CI

GitHub Actions workflow runs:
- install (`pip install -e .[dev]`)
- test (`pytest`)

## Error Handling

- Validation failures raise `ValueError` in schema validation.
- Rendering failures raise `RenderingError`.
- API converts exceptions to HTTP 400.

## Dependencies

Defined in `pyproject.toml`:
- runtime: `python-pptx`, `pillow`, `pydantic`, `fastapi`, `uvicorn`
- dev: `pytest`, `httpx`


## Installer Build

Create distributable installer artifacts:

```bash
bash installer/build_installer.sh
```

See details in `installer/README_INSTALLER.md`.


Installer build now includes both CLI and UI standalone bundles under `dist/install/` (`ppt-renderer/` and `ppt-renderer-ui/`).
