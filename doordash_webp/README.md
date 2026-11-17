# doordash_webp

Job Factory preprocessing: converts WebP images to PNG.

- `preprocess.py` - the code (`preprocess(s3, log, progress, output_uri, image_column="image_url")`)
- `requirements.txt` - packages installed before it runs (Pillow)

Input: a CSV with an `image_url` column (s3:// links to .webp files).
Output: one .png per row under the output path (same input -> same file name, safe to re-run).
