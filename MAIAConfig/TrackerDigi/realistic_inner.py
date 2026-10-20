from GaudiKernel.Constants import INFO
from Configurables import MuonCVXDDigitiser

from Common.overlay_utils import overlay_input


_INNER_TRACKER_BARREL_LAYER_IDS = [0, 1, 2]
_INNER_TRACKER_ENDCAP_LAYER_IDS = [0, 1, 2, 3, 4, 5, 6]

# The inner tracker sensors have long pixels: 25 um along u and 312 um along v, so that the
# resolution of a single pixel, pitch / sqrt(12), is the 7 um x 90 um assumed by the parametric
# digitisation (TrackerDigi/tracking_inner.py). The hit uncertainties du, dv are pitch / sqrt(12).
_INNER_TRACKER_PIXEL_SIZE_U = 0.025  # mm
_INNER_TRACKER_PIXEL_SIZE_V = 0.312  # mm


def _inner_tracker_digitiser(name, input_collection, subdetector, prefix, layer_ids, args):
    """
    MuonCVXDDigitiser for one sub-detector. The output collections are named after prefix:
    <prefix>Hits and <prefix>HitsRelations (hits and hit -> sim-hit links, as for DDPlanarDigi),
    <prefix>Pixels and <prefix>RawHitRelations (fired pixels and hit -> pixel links, filled with
    --storeFiredPixels).
    """
    return MuonCVXDDigitiser(
        name,
        CollectionName = input_collection,
        EventHeader = ["EventHeader"],
        SimHitLocCollectionName = [prefix + "Pixels"],
        OutputCollectionName = [prefix + "Hits"],
        RelationColName = [prefix + "HitsRelations"],
        RawHitsLinkColName = [prefix + "RawHitRelations"],
        SubDetectorName = subdetector,
        LayerIDs = layer_ids,
        StoreFiredPixels = getattr(args, "storeFiredPixels", False),
        PixelSizeX = _INNER_TRACKER_PIXEL_SIZE_U,
        PixelSizeY = _INNER_TRACKER_PIXEL_SIZE_V,
        OutputLevel = INFO,
    )


def ITBarrel_cfg(args):
    """
    Create a new inner barrel digitiser instance with the MuonCVXDDigitiser.
    """
    inputHitCollections = overlay_input("InnerTrackerBarrelCollection", args)
    return _inner_tracker_digitiser(
        "InnerBarrelDigitiser",
        inputHitCollections,
        "InnerTrackerBarrel",
        "ITBarrel",
        _INNER_TRACKER_BARREL_LAYER_IDS,
        args,
    )


def ITEndcap_cfg(args):
    """
    Create a new inner endcap digitiser instance with the MuonCVXDDigitiser.
    """
    inputHitCollections = overlay_input("InnerTrackerEndcapCollection", args)
    return _inner_tracker_digitiser(
        "InnerEndcapDigitiser",
        inputHitCollections,
        "InnerTrackerEndcap",
        "ITEndcap",
        _INNER_TRACKER_ENDCAP_LAYER_IDS,
        args,
    )
