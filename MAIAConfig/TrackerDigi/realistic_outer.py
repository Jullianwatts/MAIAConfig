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


def _outer_tracker_digitiser(name, input_collection, sim_local_collection, hit_collection, relation_collection, raw_relation_collection, layer_ids):
    return MuonCVXDDigitiser(
        name,
        CollectionName = input_collection,
        EventHeader = ["EventHeader"],
        SimHitLocCollectionName = [sim_local_collection],
        OutputCollectionName = [hit_collection],
        RelationColName = [relation_collection],
        RawHitsLinkColName = [raw_relation_collection],
        SubDetectorName = sim_local_collection,
        LayerIDs = layer_ids,
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
        "OTBarrelHits",
        "OTBarrelHitsRelations",
        "OTBarrelRawHitRelations",
        _OUTER_TRACKER_BARREL_LAYER_IDS,
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
        "OTEndcapHits",
        "OTEndcapHitsRelations",
        "OTEndcapRawHitRelations",
        _OUTER_TRACKER_ENDCAP_LAYER_IDS,
    )
