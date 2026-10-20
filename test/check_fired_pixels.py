#!/usr/bin/env python3
"""Check the fired pixels written by the realistic tracker digitisation with --storeFiredPixels.

Usage: check_fired_pixels.py digi_realistic_output.edm4hep.root
"""
import sys

from podio.root_io import Reader

PREFIXES = ["VXDBarrel", "VXDEndcap", "ITBarrel", "ITEndcap", "OTBarrel", "OTEndcap"]

counts = {prefix: {"hits": 0, "pixels": 0, "links": 0} for prefix in PREFIXES}
failures = []
for frame in Reader(sys.argv[1]).get("events"):
    for prefix in PREFIXES:
        hits = frame.get(prefix + "Hits")
        pixels = frame.get(prefix + "Pixels")
        links = frame.get(prefix + "RawHitRelations")
        counts[prefix]["hits"] += len(hits)
        counts[prefix]["pixels"] += len(pixels)
        counts[prefix]["links"] += len(links)
        # every pixel belongs to one hit on the same sensor, and every hit has pixels
        hits_with_pixels = set()
        for link in links:
            hit, pixel = link.getFrom(), link.getTo()
            hits_with_pixels.add(hit.id().index)
            if hit.getCellID() != pixel.getCellID():
                failures.append(f"{prefix}: pixel on another sensor than its hit")
        if len(hits_with_pixels) != len(hits):
            failures.append(f"{prefix}: {len(hits) - len(hits_with_pixels)} hits without pixels")

for prefix, c in counts.items():
    print(f"{prefix:10s} hits {c['hits']:6d}  pixels {c['pixels']:7d}  links {c['links']:7d}")
    if c["hits"] == 0 or c["pixels"] == 0:
        failures.append(f"{prefix}: no hits or no pixels")
    if c["links"] != c["pixels"]:
        failures.append(f"{prefix}: {c['pixels']} pixels but {c['links']} hit -> pixel links")

for failure in sorted(set(failures)):
    print("FAILED:", failure)
sys.exit(1 if failures else 0)
