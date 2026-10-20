from GaudiKernel.Constants import INFO
from Configurables import MuonCVXDDigitiser

from Common.overlay_utils import overlay_input


_VERTEX_BARREL_LAYER_IDS = [0, 1, 2, 4, 6]
_VERTEX_ENDCAP_LAYER_IDS = [0, 1, 2, 3, 4, 5, 6, 7]


def _vertex_digitiser(name, input_collection, subdetector, prefix, layer_ids, args):
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
        OutputLevel = INFO,
    )


def VXDBarrel_cfg(args):
    """
    Create a new vertex barrel digitiser instance with the MuonCVXDDigitiser.
    """
    inputHitCollections = overlay_input("VertexBarrelCollection", args)
    return _vertex_digitiser(
        "VXDBarrelDigitiser",
        inputHitCollections,
        "VertexBarrel",
        "VXDBarrel",
        _VERTEX_BARREL_LAYER_IDS,
        args,
    )


def VXDEndcap_cfg(args):
    """
    Create a new vertex endcap digitiser instance with the MuonCVXDDigitiser.
    """
    inputHitCollections = overlay_input("VertexEndcapCollection", args)
    return _vertex_digitiser(
        "VXDEndcapDigitiser",
        inputHitCollections,
        "VertexEndcap",
        "VXDEndcap",
        _VERTEX_ENDCAP_LAYER_IDS,
        args,
    )
