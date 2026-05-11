# Deterministic PPT Rendering Engine

## Architecture
- `Renderer`: presentation-level orchestration (slide size + multi-slide rendering).
- `SlideRenderer`: per-slide fixed-coordinate rendering dispatcher.
- `TextRenderer`: text rendering with wrap + deterministic font autosize heuristic.
- `ImageRenderer`: image rendering with `contain`, `cover`, `fit` crop modes.
- `models.py`: strict JSON schema parsing into immutable dataclasses.

## Folder Structure
```text
src/ppt_renderer/
  __init__.py
  main.py
  models.py
  renderers.py
examples/
  sample_input.json
```

## Design Principles
- No AI logic.
- Deterministic rendering.
- No layout inference; only render incoming coordinates.

## Error Handling Strategy
- Input schema/type violations raise `ValueError` during parsing.
- Rendering failures raise `RenderingError` (e.g., missing image, unsupported mode).
- Fail-fast policy: stop generation on first non-recoverable error.

## Sample JSON Input
See `examples/sample_input.json`.

## Sample Output
- Input: `examples/sample_input.json`
- Output: `output/sample_deck.pptx`

## Usage
```python
from ppt_renderer import generate_ppt_from_file

generate_ppt_from_file("examples/sample_input.json", "output/sample_deck.pptx")
```

## Dependencies
```bash
pip install python-pptx pillow
```
