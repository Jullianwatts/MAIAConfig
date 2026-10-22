#!/usr/bin/env python3
"""Check that the parametric and realistic tracker digitisers write the same hit collections,
and that these are the collections the downstream algorithms read.

The downstream algorithms (coning, double-layer filtering, hit merging, tracking) are configured
once, so whichever digitiser runs for a subdetector must produce exactly their input collections.

The realistic digitisers (MuonCVXDDigitiser) and the double-layer filter (FilterDoubleLayerHits,
which has no Gaudi port yet) are not shipped by every release image. Whatever is missing is
reported and left out of the checks; everything else is required.

Usage: PYTHONPATH=<MAIAConfig>/MAIAConfig check_tracker_collections.py
"""
import argparse
import importlib
import sys

from GaudiKernel.Configurable import Configurable

from TrackerDigi import tracking_inner, tracking_outer, tracking_vertex
from TrackerDigi.coning import tracker_coner_cfgs
from Tracking.mergers import mergehits_cfg, mergehitsrelations_cfg

skipped = []


def optional(module_name):
    """The module, or None when the image does not ship the components it configures."""
    try:
        return importlib.import_module(module_name)
    except ImportError as error:
        skipped.append(f"{module_name} ({error})")
        return None


realistic_vertex = optional("TrackerDigi.realistic_vertex")
realistic_inner = optional("TrackerDigi.realistic_inner")
realistic_outer = optional("TrackerDigi.realistic_outer")
dl_module = optional("Tracking.filterDL_vertex")

# subdetector prefix: (parametric module, realistic module)
MODULES = {
    "VXDBarrel": (tracking_vertex, realistic_vertex), "VXDEndcap": (tracking_vertex, realistic_vertex),
    "ITBarrel": (tracking_inner, realistic_inner), "ITEndcap": (tracking_inner, realistic_inner),
    "OTBarrel": (tracking_outer, realistic_outer), "OTEndcap": (tracking_outer, realistic_outer),
}

failures = []


def args(coning=False):
    return argparse.Namespace(doOverlayFull=False, doOverlayIP=False, storeFiredPixels=False,
                              doTrackerConing=coning)


def names(value):
    """A collection property as a list: an algorithm that declares a single collection has a
    plain string here, one that declares several has a list."""
    return [value] if isinstance(value, str) else list(value)


def outputs(flavour, prefix):
    """(hit collections, relation collections) written by the digitiser of a subdetector."""
    parametric_module, realistic_module = MODULES[prefix]
    if flavour == "parametric":
        alg = getattr(parametric_module, f"{prefix}_cfg")(args())
        result = names(alg.TrackerHitCollectionName), names(alg.SimTrkHitRelCollection)
    else:
        alg = getattr(realistic_module, f"{prefix}_cfg")(args())
        result = names(alg.OutputCollectionName), names(alg.RelationColName)
    # The two flavours use the same algorithm names, which Gaudi only allows once per job:
    # forget this one before the other flavour is created
    Configurable.allConfigurables.pop(alg.name(), None)
    return result


produced = {"hits": set(), "relations": set()}
for prefix in MODULES:
    parametric = outputs("parametric", prefix)
    if MODULES[prefix][1] is None:
        print(f"{prefix:10s} parametric {parametric}")
    else:
        realistic = outputs("realistic", prefix)
        print(f"{prefix:10s} parametric {parametric}  realistic {realistic}")
        if parametric != realistic:
            failures.append(f"{prefix}: parametric {parametric} and realistic {realistic} digitisers write different collections")
    produced["hits"].update(parametric[0])
    produced["relations"].update(parametric[1])

coned_hits = {name + "Coned" for name in produced["hits"]}
coned_relations = {name + "Coned" for name in produced["relations"]}


def require(consumer, inputs, available):
    missing = [name for name in names(inputs) if name not in available]
    if missing:
        failures.append(f"{consumer} reads {missing}, which no digitiser writes")


for coner in tracker_coner_cfgs(args()):
    require(coner.name(), coner.TrackerHitInputCollections, produced["hits"])
    require(coner.name(), coner.TrackerHitInputRelations, produced["relations"])
    for name in names(coner.TrackerHitOutputCollections):
        coned_hits.discard(name)  # every coned collection must be written by a coner
    for name in names(coner.TrackerHitOutputRelations):
        coned_relations.discard(name)
if coned_hits or coned_relations:
    failures.append(f"no coner writes {sorted(coned_hits | coned_relations)}")

for coning in (False, True):
    suffix = "Coned" if coning else ""
    hits = {name + suffix for name in produced["hits"]}
    relations = {name + suffix for name in produced["relations"]}
    merge_hits = mergehits_cfg(args(coning))
    merge_relations = mergehitsrelations_cfg(args(coning))
    require(f"{merge_hits.name()} (coning {coning})", merge_hits.InputCollections, hits)
    require(f"{merge_relations.name()} (coning {coning})", merge_relations.InputCollections, relations)
    if len(merge_hits.InputCollections) != len(MODULES) or len(merge_relations.InputCollections) != len(MODULES):
        failures.append(f"the mergers (coning {coning}) do not read all the {len(MODULES)} subdetectors")

if dl_module:
    for dl_filter in (dl_module.filterDL_vertexBarrel_cfg(), dl_module.filterDL_vertexEndcap_cfg()):
        require(dl_filter.name(), dl_filter.InputCollection, produced["hits"])

for module in skipped:
    print("not available, not checked:", module)
for failure in failures:
    print("FAILED:", failure)
print("OK" if not failures else f"{len(failures)} check(s) failed")
sys.exit(1 if failures else 0)
