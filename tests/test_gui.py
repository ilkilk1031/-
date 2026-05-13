from ppt_renderer.gui import SlideForm, SlideState, build_payload


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


def test_slide_state_navigation_and_editing() -> None:
    state = SlideState(slides=[SlideForm(title="S1")], current_index=0)
    state.update_current(SlideForm(title="Edited S1", prompt="p1"))

    state.add_after_current()
    state.update_current(SlideForm(title="S2", prompt="p2"))

    state.prev()
    assert state.current.title == "Edited S1"
    assert state.current.prompt == "p1"

    state.next()
    assert state.current.title == "S2"

    state.select(0)
    assert state.current.title == "Edited S1"


def test_slide_state_remove_keeps_valid_index() -> None:
    state = SlideState(slides=[SlideForm(title="S1"), SlideForm(title="S2")], current_index=1)
    state.remove_current()
    assert state.current_index == 0
    assert state.current.title == "S1"
