# Deterministic PPT Rendering Engine

Deterministic JSON-to-PPTX renderer package with Python API, CLI, and FastAPI deployment.

## Quick Start

```bash
pip install -e .
ppt-renderer --input examples/sample_input.json --output output/sample_deck.pptx
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

### FastAPI (local)
```bash
uvicorn ppt_renderer.api:app --host 0.0.0.0 --port 8000
```

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
