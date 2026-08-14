import tempfile
import unittest
from pathlib import Path

from PIL import Image

from tools import fun_sync


class FunImageTests(unittest.TestCase):
    def test_oriented_rgb_drops_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "private.jpg"
            image = Image.new("RGB", (120, 80), (80, 140, 210))
            exif = image.getexif()
            exif[271] = "Private Camera Maker"
            exif[272] = "Private Camera Model"
            exif[306] = "2026:08:13 20:27:41"
            image.save(source, exif=exif)

            clean = fun_sync.oriented_rgb(source)
            output = Path(directory) / "public.webp"
            clean.save(output, format="WEBP", quality=82)

            with Image.open(output) as published:
                self.assertEqual(published.mode, "RGB")
                self.assertEqual(dict(published.getexif()), {})
                self.assertNotIn("exif", published.info)
                self.assertNotIn("icc_profile", published.info)

    def test_perceptual_hash_survives_reencoding(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Image.new("RGB", (160, 120), "white")
            for x in range(35, 125):
                for y in range(25, 95):
                    first.putpixel((x, y), (50, 120, 190))
            jpeg = Path(directory) / "copy.jpg"
            first.save(jpeg, quality=82)
            with Image.open(jpeg) as second:
                distance = fun_sync.hash_distance(
                    fun_sync.perceptual_hash(first), fun_sync.perceptual_hash(second.convert("RGB"))
                )
            self.assertLessEqual(distance, 2)

    def test_same_named_items_share_one_group_and_description(self):
        first = {
            "id": "first",
            "name": "Quartz",
            "category": "mineral",
            "description": "The shared description.",
            "alt_text": "First view.",
            "confidence": "high",
            "uncertainty_note": "",
            "status": "published",
            "images": {"small": "a", "medium": "b", "large": "c"},
            "width": 800,
            "height": 1000,
        }
        second = {
            **first,
            "id": "second",
            "description": "This description should not create another card.",
            "alt_text": "Second view.",
        }

        groups = fun_sync.build_groups([first, second])

        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["description"], "The shared description.")
        self.assertEqual(groups[0]["photo_count"], 2)
        self.assertEqual([photo["id"] for photo in groups[0]["photos"]], ["first", "second"])


if __name__ == "__main__":
    unittest.main()
