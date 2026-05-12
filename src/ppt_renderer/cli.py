from __future__ import annotations

import argparse
import os
import sys

from .main import generate_ppt_from_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic JSON-to-PPTX renderer")
    parser.add_argument("--input", help="Input JSON path")
    parser.add_argument("--output", help="Output PPTX path")
    return parser


def _print_windows_hint(parser: argparse.ArgumentParser) -> None:
    parser.print_help()
    print("\nThis executable is a CLI tool, not a click-to-install GUI app.")
    print("Run it from terminal with arguments, for example:")
    print("  ppt-renderer.exe --input examples/sample_input.json --output output/sample_deck.pptx")
    if os.name == "nt":
        try:
            input("\nPress Enter to close...")
        except EOFError:
            pass


def main() -> None:
    parser = build_parser()
    if len(sys.argv) == 1:
        _print_windows_hint(parser)
        return

    args = parser.parse_args()
    if not args.input or not args.output:
        parser.error("Both --input and --output are required.")
    generate_ppt_from_file(args.input, args.output)


if __name__ == "__main__":
    main()
