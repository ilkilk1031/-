from ppt_renderer.cli import build_parser


def test_cli_parser():
    parser = build_parser()
    args = parser.parse_args(["--input", "a.json", "--output", "b.pptx"])
    assert args.input == "a.json"
    assert args.output == "b.pptx"
