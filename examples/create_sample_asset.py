from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    out = Path(__file__).parent / "assets" / "sample.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (640, 360), (240, 244, 248))
    draw = ImageDraw.Draw(img)
    draw.rectangle((20, 20, 620, 340), outline=(31, 41, 55), width=4)
    draw.text((40, 160), "sample image", fill=(31, 41, 55))
    img.save(out)
    print(f"created: {out}")


if __name__ == "__main__":
    main()
