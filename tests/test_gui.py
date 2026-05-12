from ppt_renderer.gui import SlideForm, build_payload


def test_build_payload_single_slide() -> None:
    slide = SlideForm(
        title="Title",
        prompt="Prompt",
        input_image="input.png",
        output_image="output.png",
        references=["ref1.png", "ref2.png"],
    )
    payload = build_payload([slide])
    assert payload["slide_size"]["width"] > 0
    assert len(payload["slides"]) == 1
    elements = payload["slides"][0]["elements"]
    assert any(e.get("type") == "image" and e.get("path") == "input.png" for e in elements)
    assert any(e.get("type") == "image" and e.get("path") == "output.png" for e in elements)
    assert any(e.get("type") == "text" and "Prompt" in e.get("text", "") for e in elements)
