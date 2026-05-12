from __future__ import annotations

import argparse

from .main import generate_ppt_from_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic JSON-to-PPTX renderer")
    parser.add_argument("--input", required=True, help="Input JSON path")
    parser.add_argument("--output", required=True, help="Output PPTX path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    generate_ppt_from_file(args.input, args.output)


if __name__ == "__main__":
    main()
