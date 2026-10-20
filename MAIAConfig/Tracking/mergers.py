from GaudiKernel.Constants import INFO, WARNING, DEBUG
from Configurables import CollectionMerger
from Common.tracker_collections import hit_collection, hit_relation_collection

def _coned(name, args):
    """Append "Coned" to a collection name when tracker coning is enabled."""
    return name + "Coned" if getattr(args, "doTrackerConing", False) else name

# Order in which the subdetector collections are merged
_MERGE_ORDER = ["VXDBarrel", "ITBarrel", "OTBarrel", "VXDEndcap", "ITEndcap", "OTEndcap"]

def mergehits_cfg(args):
    """
    Create a new CollectionMerger instance for merging hits.
    """
    bases = [hit_collection(prefix) for prefix in _MERGE_ORDER]
    return CollectionMerger(
        "MergeHits",
        InputCollections = [_coned(b, args) for b in bases],
        OutputCollection = "MergedTrackerHits",
        OutputLevel = INFO
    )

def mergehitsrelations_cfg(args):
    """
    Create a new CollectionMerger instance for merging hits relations.
    """
    bases = [hit_relation_collection(prefix) for prefix in _MERGE_ORDER]
    return CollectionMerger(
        "MergeHitsRelations",
        InputCollections = [_coned(b, args) for b in bases],
        OutputCollection = "MergedTrackerHitsRelations",
        OutputLevel = INFO
    )
