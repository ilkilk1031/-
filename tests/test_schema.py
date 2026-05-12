from ppt_renderer.schema import validate_payload


def test_validate_payload_ok():
    payload = {
        "slide_size": {"width": 12192000, "height": 6858000},
        "slides": [{"elements": [{"type": "text", "box": {"x": 1, "y": 1, "width": 10, "height": 10}, "text": "ok"}]}],
    }
    result = validate_payload(payload)
    assert result["slide_size"]["width"] == 12192000


def test_validate_payload_invalid_color():
    payload = {
        "slide_size": {"width": 12192000, "height": 6858000},
        "slides": [{"elements": [{"type": "text", "box": {"x": 1, "y": 1, "width": 10, "height": 10}, "text": "ok", "style": {"color_hex": "BADHEX1"}}]}],
    }
    try:
        validate_payload(payload)
        assert False
    except ValueError:
        assert True
