from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from .main import generate_ppt

DEFAULT_SLIDE_SIZE = {"width": 12192000, "height": 6858000}


@dataclass
class SlideForm:
    title: str = ""
    prompt: str = ""
    input_image: str = ""
    output_image: str = ""
    references: list[str] = field(default_factory=list)


TEMPLATES = {
    "single_case": {
        "title": {"x": 500000, "y": 220000, "width": 11000000, "height": 700000},
        "prompt": {"x": 500000, "y": 5450000, "width": 11000000, "height": 1200000},
        "input": {"x": 500000, "y": 1100000, "width": 5200000, "height": 4100000},
        "output": {"x": 6500000, "y": 1100000, "width": 5200000, "height": 4100000},
        "ref_boxes": [
            {"x": 500000, "y": 5050000, "width": 2500000, "height": 350000},
            {"x": 3100000, "y": 5050000, "width": 2500000, "height": 350000},
            {"x": 5700000, "y": 5050000, "width": 2500000, "height": 350000},
        ],
    }
}


def build_payload(slides: list[SlideForm], template_name: str = "single_case") -> dict:
    template = TEMPLATES[template_name]
    result_slides: list[dict] = []

    for slide in slides:
        elements: list[dict] = []
        elements.append({"type": "text", "box": template["title"], "text": slide.title or "Untitled"})

        if slide.input_image:
            elements.append(
                {
                    "type": "image",
                    "box": template["input"],
                    "path": slide.input_image,
                    "crop_mode": "cover",
                }
            )
        if slide.output_image:
            elements.append(
                {
                    "type": "image",
                    "box": template["output"],
                    "path": slide.output_image,
                    "crop_mode": "cover",
                }
            )

        for idx, ref in enumerate(slide.references[:3]):
            elements.append(
                {
                    "type": "text",
                    "box": template["ref_boxes"][idx],
                    "text": f"Ref {idx+1}: {Path(ref).name}",
                }
            )
            elements.append(
                {
                    "type": "image",
                    "box": {
                        "x": template["ref_boxes"][idx]["x"],
                        "y": template["ref_boxes"][idx]["y"] - 900000,
                        "width": template["ref_boxes"][idx]["width"],
                        "height": 850000,
                    },
                    "path": ref,
                    "crop_mode": "cover",
                }
            )

        elements.append({"type": "text", "box": template["prompt"], "text": slide.prompt or ""})
        result_slides.append({"elements": elements})

    return {"slide_size": DEFAULT_SLIDE_SIZE, "slides": result_slides}


class RendererGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("PPT Renderer UI")
        self.root.geometry("980x680")

        self.slides: list[SlideForm] = [SlideForm(title="Slide 1")]
        self.current_index = 0

        self._build_ui()
        self._refresh_list()
        self._load_slide_to_form(0)

    def _build_ui(self) -> None:
        left = tk.Frame(self.root)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        self.listbox = tk.Listbox(left, width=28, height=30)
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self._on_select_slide)

        tk.Button(left, text="+ Slide", command=self._add_slide).pack(fill=tk.X, pady=3)
        tk.Button(left, text="- Slide", command=self._remove_slide).pack(fill=tk.X, pady=3)

        right = tk.Frame(self.root)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.title_var = tk.StringVar()
        tk.Label(right, text="Title").pack(anchor="w")
        tk.Entry(right, textvariable=self.title_var).pack(fill=tk.X)

        tk.Label(right, text="Input Image").pack(anchor="w", pady=(10, 0))
        self.input_var = tk.StringVar()
        tk.Entry(right, textvariable=self.input_var).pack(fill=tk.X)
        tk.Button(right, text="Browse Input", command=lambda: self._pick_file(self.input_var)).pack(anchor="w")

        tk.Label(right, text="Output Image").pack(anchor="w", pady=(10, 0))
        self.output_var = tk.StringVar()
        tk.Entry(right, textvariable=self.output_var).pack(fill=tk.X)
        tk.Button(right, text="Browse Output", command=lambda: self._pick_file(self.output_var)).pack(anchor="w")

        tk.Label(right, text="Reference Images (one path per line, up to 3)").pack(anchor="w", pady=(10, 0))
        self.refs_text = ScrolledText(right, height=5)
        self.refs_text.pack(fill=tk.X)

        tk.Label(right, text="Prompt").pack(anchor="w", pady=(10, 0))
        self.prompt_text = ScrolledText(right, height=8)
        self.prompt_text.pack(fill=tk.BOTH, expand=True)

        actions = tk.Frame(right)
        actions.pack(fill=tk.X, pady=8)
        tk.Button(actions, text="Save Slide", command=self._save_current_slide).pack(side=tk.LEFT)
        tk.Button(actions, text="Export JSON", command=self._export_json).pack(side=tk.LEFT, padx=6)
        tk.Button(actions, text="Generate PPT", command=self._generate_ppt).pack(side=tk.RIGHT)

    def _refresh_list(self) -> None:
        self.listbox.delete(0, tk.END)
        for i, s in enumerate(self.slides, start=1):
            name = s.title.strip() or f"Slide {i}"
            self.listbox.insert(tk.END, f"{i}. {name}")

    def _on_select_slide(self, _event=None) -> None:
        if not self.listbox.curselection():
            return
        self._save_current_slide()
        self.current_index = int(self.listbox.curselection()[0])
        self._load_slide_to_form(self.current_index)

    def _load_slide_to_form(self, idx: int) -> None:
        slide = self.slides[idx]
        self.title_var.set(slide.title)
        self.input_var.set(slide.input_image)
        self.output_var.set(slide.output_image)
        self.refs_text.delete("1.0", tk.END)
        self.refs_text.insert("1.0", "\n".join(slide.references))
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert("1.0", slide.prompt)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)

    def _save_current_slide(self) -> None:
        refs = [line.strip() for line in self.refs_text.get("1.0", tk.END).splitlines() if line.strip()]
        self.slides[self.current_index] = SlideForm(
            title=self.title_var.get().strip(),
            prompt=self.prompt_text.get("1.0", tk.END).strip(),
            input_image=self.input_var.get().strip(),
            output_image=self.output_var.get().strip(),
            references=refs[:3],
        )
        self._refresh_list()

    def _add_slide(self) -> None:
        self._save_current_slide()
        self.slides.append(SlideForm(title=f"Slide {len(self.slides)+1}"))
        self.current_index = len(self.slides) - 1
        self._refresh_list()
        self._load_slide_to_form(self.current_index)

    def _remove_slide(self) -> None:
        if len(self.slides) == 1:
            messagebox.showwarning("Warning", "At least one slide is required.")
            return
        del self.slides[self.current_index]
        self.current_index = max(0, self.current_index - 1)
        self._refresh_list()
        self._load_slide_to_form(self.current_index)

    def _pick_file(self, target_var: tk.StringVar) -> None:
        path = filedialog.askopenfilename(title="Select image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")])
        if path:
            target_var.set(path)

    def _export_json(self) -> None:
        self._save_current_slide()
        payload = build_payload(self.slides)
        out = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not out:
            return
        Path(out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        messagebox.showinfo("Done", f"Saved JSON: {out}")

    def _generate_ppt(self) -> None:
        self._save_current_slide()
        output = filedialog.asksaveasfilename(defaultextension=".pptx", filetypes=[("PowerPoint", "*.pptx")])
        if not output:
            return
        try:
            payload = build_payload(self.slides)
            generate_ppt(payload, output)
            messagebox.showinfo("Success", f"Generated: {output}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = RendererGUI()
    app.run()


if __name__ == "__main__":
    main()
