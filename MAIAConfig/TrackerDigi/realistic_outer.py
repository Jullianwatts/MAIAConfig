from GaudiKernel.Constants import INFO
from Configurables import MuonCVXDDigitiser

from Common.overlay_utils import overlay_input


_OUTER_TRACKER_BARREL_LAYER_IDS = [0, 1, 2]
_OUTER_TRACKER_ENDCAP_LAYER_IDS = [0, 1, 2, 3]

# The outer tracker sensors have long pixels: 25 um along u and 312 um along v, so that the
# resolution of a single pixel, pitch / sqrt(12), is the 7 um x 90 um assumed by the parametric
# digitisation (TrackerDigi/tracking_outer.py). The hit uncertainties du, dv are pitch / sqrt(12).
_OUTER_TRACKER_PIXEL_SIZE_U = 0.025  # mm
_OUTER_TRACKER_PIXEL_SIZE_V = 0.312  # mm


def _outer_tracker_digitiser(name, input_collection, subdetector, prefix, layer_ids, args):
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
        PixelSizeX = _OUTER_TRACKER_PIXEL_SIZE_U,
        PixelSizeY = _OUTER_TRACKER_PIXEL_SIZE_V,
        OutputLevel = INFO,
    )


def OTBarrel_cfg(args):
    """
    Create a new outer barrel digitiser instance with the MuonCVXDDigitiser.
    """
    inputHitCollections = overlay_input("OuterTrackerBarrelCollection", args)
    return _outer_tracker_digitiser(
        "OTBarrelDigitiser",
        inputHitCollections,
        "OuterTrackerBarrel",
        "OTBarrel",
        _OUTER_TRACKER_BARREL_LAYER_IDS,
        args,
    )


def OTEndcap_cfg(args):
    """
    Create a new outer endcap digitiser instance with the MuonCVXDDigitiser.
    """
    inputHitCollections = overlay_input("OuterTrackerEndcapCollection", args)
    return _outer_tracker_digitiser(
        "OTEndcapDigitiser",
        inputHitCollections,
        "OuterTrackerEndcap",
        "OTEndcap",
        _OUTER_TRACKER_ENDCAP_LAYER_IDS,
        args,
    )
