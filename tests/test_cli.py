from ppt_renderer.cli import build_parser, main


def test_cli_parser():
    parser = build_parser()
    args = parser.parse_args(["--input", "a.json", "--output", "b.pptx"])
    assert args.input == "a.json"
    assert args.output == "b.pptx"


def test_cli_no_args_prints_hint(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["ppt-renderer"])
    main()
    out = capsys.readouterr().out
    assert "CLI tool" in out
    assert "--input" in out and "--output" in out
