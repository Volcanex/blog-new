#!/usr/bin/env python3
import json
import os
import subprocess
import time
from fractions import Fraction
from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS

MASTERS = Path("/home/gabriel/photo-sync-server/storage/photos/masters")
RAW = Path("/home/gabriel/photo-sync-server/storage/photos/raw")
OUT = Path("/home/gabriel/blog-new/data/photography/manifest.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

MIN_PHOTO_BYTES = 50_000
MASTER_EXTS = {".jpg", ".jpeg"}
RAW_EXTS = {".arw", ".cr2", ".cr3", ".nef", ".orf", ".raf", ".rw2", ".dng", ".raw"}


def load_existing():
    try:
        with open(OUT) as f:
            data = json.load(f)
        return {
            "masters": dict(data.get("masters", {})),
            "raw": dict(data.get("raw", {})),
        }
    except Exception:
        return {"masters": {}, "raw": {}}


def shutter_str(exposure_time):
    try:
        et = float(exposure_time)
        if et >= 1:
            return f"{et:.1f}s"
        frac = Fraction(et).limit_denominator(10000)
        return f"1/{frac.denominator}"
    except Exception:
        return str(exposure_time)


def extract_exif(path):
    try:
        with Image.open(path) as img:
            w, h = img.size
            raw = img._getexif()
        out = {"width": int(w), "height": int(h)}
        if not raw:
            return out
        exif = {TAGS.get(tag_id, str(tag_id)): val for tag_id, val in raw.items()}
        dt = exif.get("DateTimeOriginal", "")
        if dt:
            out["date_taken"] = dt[:10].replace(":", "-")
            out["datetime_sort"] = dt.replace(":", "-", 2)
        if "Model" in exif:
            out["camera"] = exif["Model"].strip()
        if "LensModel" in exif:
            out["lens"] = exif["LensModel"].strip()
        fl = exif.get("FocalLength")
        if fl is not None:
            try:
                out["focal_length"] = f"{int(float(fl))}mm"
            except Exception:
                pass
        fn = exif.get("FNumber")
        if fn is not None:
            try:
                out["aperture"] = f"f/{float(fn):.1f}"
            except Exception:
                pass
        et = exif.get("ExposureTime")
        if et is not None:
            out["shutter"] = shutter_str(et)
        iso = exif.get("ISOSpeedRatings")
        if iso is not None:
            out["iso"] = f"ISO {iso}"
        return out
    except Exception as e:
        return {"_exif_error": str(e)}


def list_remote_files(category):
    tracker_path = Path("/home/gabriel/photo-sync-server/file_tracker.json")
    try:
        tracker = json.loads(tracker_path.read_text())
    except Exception as e:
        raise RuntimeError(f"Could not read photo-sync tracker: {e}")
    files = []
    for name, info in tracker.get(category, {}).items():
        try:
            size = int(info.get("size", 0))
        except Exception:
            size = 0
        files.append((name, size, info.get("uploaded", "")))
    return sorted(files)


def scan_category(directory, category, exts, min_bytes, existing, do_exif):
    manifest = {}
    reused = 0
    updated = 0
    skipped = 0
    files = list_remote_files(category)
    total = len(files)
    for i, (name, size, modtime) in enumerate(files, 1):
        if name.startswith(".") or Path(name).suffix.lower() not in exts:
            skipped += 1
            continue
        if size < min_bytes:
            skipped += 1
            continue
        old = existing.get(name)
        if old and old.get("size_bytes") == size:
            manifest[name] = old
            reused += 1
        else:
            entry = {"size_bytes": size, "mtime": modtime}
            if do_exif:
                entry.update(extract_exif(directory / name))
            manifest[name] = entry
            updated += 1
        if i % 50 == 0:
            print(f"  [{i}/{total}] reused={reused} updated={updated} skipped={skipped}", flush=True)
    return manifest, reused, updated, skipped


def write_manifest(masters, raws):
    manifest = {
        "version": 2,
        "generated_at": time.time(),
        "masters": masters,
        "raw": raws,
    }
    tmp = OUT.with_suffix(".tmp")
    tmp.write_text(json.dumps(manifest, default=str))
    os.replace(tmp, OUT)


def main():
    t0 = time.time()
    existing = load_existing()
    old_masters = len(existing.get("masters", {}))
    old_raw = len(existing.get("raw", {}))
    print(f"Building photo manifest to {OUT}")
    print(f"Existing: {old_masters} masters + {old_raw} raw")

    print("")
    print(f"Masters ({MASTERS}):")
    masters, mr, mu, ms = scan_category(MASTERS, "masters", MASTER_EXTS, MIN_PHOTO_BYTES, existing.get("masters", {}), True)
    write_manifest(masters, existing.get("raw", {}))
    print(f"  masters done: {len(masters)} entries, reused={mr}, updated={mu}, skipped={ms}")

    print("")
    print(f"Raw ({RAW}):")
    raws, rr, ru, rs = scan_category(RAW, "raw", RAW_EXTS, MIN_PHOTO_BYTES, existing.get("raw", {}), False)
    write_manifest(masters, raws)
    print("")
    print(f"Wrote {OUT}: {len(masters)} masters + {len(raws)} raws in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
