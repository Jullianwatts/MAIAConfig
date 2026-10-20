from GaudiKernel.Constants import INFO, WARNING
from Configurables import DDPlanarDigi
from Common.overlay_utils import overlay_input
from Common.tracker_collections import hit_collection, hit_relation_collection

def VXDBarrel_cfg(args):
    """
    Create a new vertex barrel instance with the given parameters.
    """
    inputHitCollections = overlay_input("VertexBarrelCollection", args)
    return DDPlanarDigi(
        "VXDBarrelDigitiser",
        CorrectTimesForPropagation = False,
        CorrectTimeWindowForPropagation = True,
        IsStrip = False,
        ResolutionT = [0.03],
        ResolutionU = [0.005],
        ResolutionV = [0.005],
        SubDetectorName = "Vertex",
        TimeWindowMax = [0.15],
        TimeWindowMin = [-0.09],
        UseTimeWindow = True,
        SimTrackHitCollectionName = inputHitCollections,
        SimTrkHitRelCollection = [hit_relation_collection("VXDBarrel")],
        TrackerHitCollectionName = [hit_collection("VXDBarrel")],
        ForceHitsOntoSurface = True,
        OutputLevel = INFO
    )

def VXDEndcap_cfg(args):
    """
    Create a new vertex endcap instance with the given parameters.
    """
    inputHitCollections = overlay_input("VertexEndcapCollection", args)
    return DDPlanarDigi(
        "VXDEndcapDigitiser",
        CorrectTimesForPropagation = False,
        CorrectTimeWindowForPropagation = True,
        IsStrip = False,
        ResolutionT = [0.03],
        ResolutionU = [0.005],
        ResolutionV = [0.005],
        SubDetectorName = "Vertex",
        TimeWindowMax = [0.15],
        TimeWindowMin = [-0.09],
        UseTimeWindow = True,
        SimTrackHitCollectionName = inputHitCollections,
        SimTrkHitRelCollection = [hit_relation_collection("VXDEndcap")],
        TrackerHitCollectionName = [hit_collection("VXDEndcap")],
        ForceHitsOntoSurface = True,
        OutputLevel = INFO
    )
