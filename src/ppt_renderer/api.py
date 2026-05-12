from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .main import generate_ppt

app = FastAPI(title="ppt-renderer")


@app.post("/generate-ppt")
def generate_ppt_endpoint(payload: dict):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "result.pptx"
            generate_ppt(payload, str(output_path))
            return FileResponse(
                str(output_path),
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                filename="generated.pptx",
            )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
