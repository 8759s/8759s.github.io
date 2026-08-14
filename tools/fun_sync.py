#!/usr/bin/env python3
"""Build the Fun gallery from private local photographs.

The source inbox is intentionally git-ignored. Published images are newly
encoded from oriented RGB pixels, so EXIF, GPS, XMP, IPTC, embedded thumbnails,
camera details, timestamps, and original filenames are not carried forward.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Literal

from PIL import Image, ImageOps
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "fun_photos"
DATA_FILE = ROOT / "data" / "fun" / "items.json"
OVERRIDES_FILE = ROOT / "data" / "fun" / "overrides.json"
IMAGE_DIR = ROOT / "static" / "fun" / "images"
SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
VARIANT_EDGES = {"small": 480, "medium": 960, "large": 1600}
PROMPT_VERSION = "2026-08-13.1"
DEFAULT_MODEL = "gemini-3.5-flash"


class SpecimenAnalysis(BaseModel):
    name: str = Field(description="Short, familiar name for the specimen.")
    category: Literal["gemstone", "mineral", "fossil", "rock", "unknown"]
    description: str = Field(description="A 45 to 70 word explanation for ages 6 to 10.")
    alt_text: str = Field(description="Literal visual description, at most 30 words.")
    confidence: Literal["high", "medium", "low"]
    uncertainty_note: str = Field(description="Brief caveat or an empty string when none is needed.")
    privacy_risk: bool = Field(description="True if visible pixels show personal or location information.")
    privacy_note: str = Field(description="Visible privacy concern or an empty string.")


PROMPT = """
You are a careful museum educator specializing in geology and paleontology.
Study this photograph of one specimen and return the requested structured data.

Identify from visible evidence only. Do not invent a mine, location, age, owner,
price, treatment, chemical test, or provenance. Many minerals look alike in a
photo, so use a familiar likely name and explain uncertainty when necessary.

Write a warm 45-to-70-word description for children ages 6 to 10. It should take
about 20 to 30 seconds to read aloud, point out something the child can see, and
teach one accurate, memorable fact. Avoid sales language and avoid saying an
uncertain identification is proven. The alt text must describe appearance rather
than repeat the lesson. Set privacy_risk only for information visible in the
pixels, such as a face, address, license plate, document, or recognizable private
location. Camera metadata has already been removed.
""".strip()


def load_json(path: Path, fallback):
    if not path.exists():
        return fallback
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def atomic_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, suffix=".tmp"
    ) as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temp_path = Path(handle.name)
    temp_path.replace(path)


def source_files() -> list[Path]:
    if not INBOX.exists():
        return []
    return sorted(
        path
        for path in INBOX.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def source_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def oriented_rgb(path: Path) -> Image.Image:
    with Image.open(path) as opened:
        opened.load()
        oriented = ImageOps.exif_transpose(opened)
        if oriented.mode in {"RGBA", "LA"}:
            rgba = oriented.convert("RGBA")
            background = Image.new("RGBA", rgba.size, "white")
            background.alpha_composite(rgba)
            rgb = background.convert("RGB")
        else:
            rgb = oriented.convert("RGB")

        # Copy pixels into a fresh object. No source metadata is copied.
        clean = Image.new("RGB", rgb.size)
        clean.paste(rgb)
        return clean


def perceptual_hash(image: Image.Image) -> str:
    sample = image.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
    pixels = list(sample.get_flattened_data())
    bits = []
    for row in range(8):
        offset = row * 9
        bits.extend(pixels[offset + col] > pixels[offset + col + 1] for col in range(8))
    value = sum(int(bit) << index for index, bit in enumerate(bits))
    return f"{value:016x}"


def hash_distance(left: str, right: str) -> int:
    return (int(left, 16) ^ int(right, 16)).bit_count()


def specimen_id(image: Image.Image) -> str:
    sample = image.copy()
    sample.thumbnail((512, 512), Image.Resampling.LANCZOS)
    digest = hashlib.sha256()
    digest.update(f"{sample.width}x{sample.height}".encode())
    digest.update(sample.tobytes())
    return digest.hexdigest()[:14]


def create_variants(image: Image.Image, item_id: str) -> tuple[dict[str, str], int, int]:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    large_size = image.size
    for label, max_edge in VARIANT_EDGES.items():
        variant = image.copy()
        variant.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
        destination = IMAGE_DIR / f"{item_id}-{label}.webp"
        variant.save(destination, format="WEBP", quality=82, method=6)
        paths[label] = destination.relative_to(ROOT / "static").as_posix()
        if label == "large":
            large_size = variant.size
    return paths, large_size[0], large_size[1]


def analyze(image_path: Path, model: str) -> SpecimenAnalysis:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Run `source ~/.bashrc` first, then try again."
        )

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=[
            PROMPT,
            types.Part.from_bytes(data=image_path.read_bytes(), mime_type="image/webp"),
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=SpecimenAnalysis.model_json_schema(),
            max_output_tokens=2000,
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel.MINIMAL,
            ),
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini returned no text.")
    return SpecimenAnalysis.model_validate_json(response.text)


def apply_overrides(item: dict, overrides: dict) -> dict:
    allowed = {
        "name",
        "category",
        "description",
        "alt_text",
        "confidence",
        "uncertainty_note",
        "status",
    }
    for key, value in overrides.get(item["id"], {}).items():
        if key not in allowed:
            raise ValueError(f"Unsupported override field {key!r} for {item['id']}")
        item[key] = value
    return item


def validate_items(items: list[dict]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for item in items:
        item_id = item.get("id", "<missing>")
        if item_id in seen:
            errors.append(f"duplicate item id: {item_id}")
        seen.add(item_id)
        for field in ("name", "category", "description", "alt_text", "images", "status"):
            if not item.get(field):
                errors.append(f"{item_id}: missing {field}")
        words = len(item.get("description", "").split())
        if not 35 <= words <= 80:
            errors.append(f"{item_id}: description is {words} words (expected 35-80)")
        for relative_path in item.get("images", {}).values():
            path = ROOT / "static" / relative_path
            if not path.exists():
                errors.append(f"{item_id}: missing generated image {relative_path}")
    return errors


def sync(model: str, dry_run: bool, refresh_ai: bool) -> int:
    files = source_files()
    if not files:
        print(f"No supported images found in {INBOX.relative_to(ROOT)}/")
        return 1

    items: list[dict] = load_json(DATA_FILE, [])
    overrides: dict = load_json(OVERRIDES_FILE, {})
    by_source = {item.get("source_sha256"): item for item in items}
    known_visuals = [
        (item.get("perceptual_hash"), item.get("aspect_ratio"), item)
        for item in items
        if item.get("perceptual_hash") and item.get("aspect_ratio")
    ]
    pending: list[tuple[Path, str, Image.Image, str, float]] = []

    print(f"Found {len(files)} source image(s).")
    for path in files:
        digest = source_hash(path)
        if digest in by_source and not refresh_ai:
            print(f"  cached  {path.name}")
            continue

        image = oriented_rgb(path)
        visual_hash = perceptual_hash(image)
        ratio = round(image.width / image.height, 5)
        duplicate = next(
            (
                item
                for known_hash, known_ratio, item in known_visuals
                if abs(ratio - float(known_ratio)) < 0.02
                and hash_distance(visual_hash, known_hash) <= 2
            ),
            None,
        )
        if duplicate and not refresh_ai:
            print(f"  duplicate {path.name} (matches {duplicate['id']})")
            continue
        pending.append((path, digest, image, visual_hash, ratio))
        known_visuals.append((visual_hash, ratio, {"id": specimen_id(image)}))
        print(f"  new     {path.name}")

    if dry_run:
        print(f"Dry run: {len(pending)} new image(s); Gemini was not called and no files were written.")
        return 0

    for path, digest, image, visual_hash, ratio in pending:
        item_id = specimen_id(image)
        print(f"Processing {path.name} as {item_id}...")
        image_paths, width, height = create_variants(image, item_id)
        analysis_path = ROOT / "static" / image_paths["medium"]
        analysis = analyze(analysis_path, model)
        raw = analysis.model_dump()
        word_count = len(raw["description"].split())
        if raw["privacy_risk"]:
            status = "withheld"
        else:
            status = "published"

        item = {
            "id": item_id,
            "name": raw["name"].strip(),
            "category": raw["category"],
            "description": raw["description"].strip(),
            "alt_text": raw["alt_text"].strip(),
            "confidence": raw["confidence"],
            "uncertainty_note": raw["uncertainty_note"].strip(),
            "privacy_risk": raw["privacy_risk"],
            "privacy_note": raw["privacy_note"].strip(),
            "needs_review": raw["privacy_risk"] or raw["confidence"] == "low" or not 35 <= word_count <= 80,
            "status": status,
            "images": image_paths,
            "width": width,
            "height": height,
            "source_sha256": digest,
            "perceptual_hash": visual_hash,
            "aspect_ratio": ratio,
            "metadata_stripped": True,
            "model": model,
            "prompt_version": PROMPT_VERSION,
        }
        item = apply_overrides(item, overrides)

        # Replace the same visual when explicitly refreshing; otherwise append.
        items = [existing for existing in items if existing.get("id") != item_id]
        items.append(item)
        atomic_json(DATA_FILE, items)
        print(f"  {item['name']} [{item['confidence']}; {item['status']}]")

    # Apply current corrections even when no API work was needed.
    items = [apply_overrides(item, overrides) for item in items]
    atomic_json(DATA_FILE, items)

    errors = validate_items(items)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    review = [item for item in items if item.get("needs_review") or item.get("status") != "published"]
    print(f"Gallery ready: {len(items)} item(s), {len(review)} flagged for review.")
    return 0


def validate() -> int:
    items = load_json(DATA_FILE, [])
    errors = validate_items(items)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Validated {len(items)} gallery item(s).")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    sync_parser = subparsers.add_parser("sync", help="Process new inbox photographs.")
    sync_parser.add_argument("--dry-run", action="store_true", help="Scan only; do not write or call Gemini.")
    sync_parser.add_argument("--refresh-ai", action="store_true", help="Re-run Gemini even for processed images.")
    sync_parser.add_argument(
        "--model",
        default=os.environ.get("GEMINI_VISION_MODEL", DEFAULT_MODEL),
        help=f"Gemini model (default: {DEFAULT_MODEL}).",
    )
    subparsers.add_parser("validate", help="Validate generated data and assets without API calls.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "validate":
        return validate()
    return sync(args.model, args.dry_run, args.refresh_ai)


if __name__ == "__main__":
    raise SystemExit(main())
