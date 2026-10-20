'''-------------------------------------------------------------'''
'''  Names of the tracker hit collections                       '''
'''-------------------------------------------------------------'''
# The parametric (DDPlanarDigi) and the realistic (MuonCVXDDigitiser) digitisers
# write their hits and hit <-> sim-hit links to the same collections, so that the
# coning, double-layer filtering, hit merging and tracking downstream work with
# either of them. Every configuration that names these collections takes the
# names from here.

# Collection prefix of each tracker subdetector, with its SimTrackerHit collection
TRACKER_SUBDETECTORS = [
    ("VXDBarrel", "VertexBarrelCollection"),
    ("VXDEndcap", "VertexEndcapCollection"),
    ("ITBarrel", "InnerTrackerBarrelCollection"),
    ("ITEndcap", "InnerTrackerEndcapCollection"),
    ("OTBarrel", "OuterTrackerBarrelCollection"),
    ("OTEndcap", "OuterTrackerEndcapCollection"),
]


def hit_collection(prefix):
    """Digitised tracker hits (TrackerHitPlane) of a subdetector."""
    return f"{prefix}Hits"


def hit_relation_collection(prefix):
    """Links from the digitised tracker hits of a subdetector to their SimTrackerHits."""
    return f"{prefix}HitsRelations"
