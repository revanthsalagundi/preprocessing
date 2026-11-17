# Reads the input CSV, downloads each WebP image, converts it to PNG and saves it in the OUTPUT folder you give.
# It writes only the PNG files (no CSV). The tool creates the jobs afterwards from the PNGs in that folder.
import io
import os

from PIL import Image


def preprocess(s3, log, progress, output_uri, image_column="image_url"):
    out = lambda name: output_uri.rstrip("/") + "/" + name
    rows = list(s3.iter_csv())                      # only the first 5 rows on "Try on a sample"
    converted, skipped = 0, 0
    for i, row in enumerate(rows, 1):
        link = row[image_column]
        name = os.path.splitext(link.split("?")[0].rsplit("/", 1)[-1])[0] + ".png"    # same input -> same name
        try:
            if s3.exists(out(name)):                # safe to re-run: files already converted are skipped
                skipped += 1
            else:
                img = Image.open(io.BytesIO(s3.download(link)))       # animated WebP: first frame
                buf = io.BytesIO()
                img.save(buf, "PNG")
                s3.upload(out(name), buf.getvalue(), "image/png")
                converted += 1
        except Exception as e:
            log(f"row {i}: could not convert {link}: {e}")
        progress(i, len(rows))
    return f"{converted} converted, {skipped} already there"
