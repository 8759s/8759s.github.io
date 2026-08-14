# Fun gallery workflow

`fun_photos/` is a private, Git-ignored inbox. Copy new JPEG, PNG, WebP, or TIFF
photos there, then run:

```bash
source ~/.bashrc
.venv/bin/python tools/fun_sync.py sync
hugo server
```

Install the local dependencies once with:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-fun.txt
```

The sync command re-encodes oriented RGB pixels into 480, 960, and 1600 pixel
WebP variants. It does not copy EXIF, GPS, XMP, IPTC, embedded thumbnails,
capture timestamps, camera details, or original filenames. Only the sanitized
960-pixel version is sent to Gemini.

Gemini results are cached in `data/fun/items.json`; an ordinary rerun does not
spend quota on an already processed file. Use `--dry-run` to preview discovery
without calling Gemini. Use `--refresh-ai` only when you intentionally want to
pay the quota cost of analyzing all inbox photos again.

Photos identified with the same name are combined into one card in
`data/fun/groups.json`. The card keeps one description and offers thumbnails for
switching among its photos. Set a photo's `group` override to force matching
photos into the same card when their generated names differ.

Corrections can be placed in `data/fun/overrides.json`, keyed by generated item
ID. Supported fields are `name`, `category`, `description`, `alt_text`,
`confidence`, `uncertainty_note`, `status`, and `group`.

The Listen button uses the visitor's browser speech engine, so narration does
not consume Gemini quota or publish additional audio files.

The default vision model is `gemini-3.5-flash`, which supports free-tier input
and output. Override it with `GEMINI_VISION_MODEL` or `--model` if needed.
