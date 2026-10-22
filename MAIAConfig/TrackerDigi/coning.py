'''-------------------------------------------------------------'''
'''  Tracker hit cone filtering (BIB cleaning)                   '''
'''-------------------------------------------------------------'''
# One TrackerHitHelixFilter instance per tracker subdetector. Each keeps the digitised
# hits that lie inside a cone around the trajectory of a signal MC particle,
# together with the corresponding sim hits and reco-to-sim relations, and writes
# them to "...Coned" collections. This is the Gaudi-native equivalent (k4Reco
# BIBUtils, formerly FilterConeHits) of the six coners in the Marlin steer_reco.py.
from GaudiKernel.Constants import INFO
from Configurables import TrackerHitHelixFilter
from Common.tracker_collections import TRACKER_SUBDETECTORS, hit_collection, hit_relation_collection

# The digitiser output names, the same for the parametric and the realistic
# digitisers, come from Common/tracker_collections.py.


def _coner_cfg(prefix, sim_collection):
    return TrackerHitHelixFilter(
        f"{prefix}Coner",
        MCParticleCollection = "MCParticles",
        TrackerHitInputCollections = hit_collection(prefix),
        TrackerHitInputRelations = hit_relation_collection(prefix),
        TrackerHitOutputCollections = hit_collection(prefix) + "Coned",
        TrackerSimHitOutputCollections = f"{sim_collection}Coned",
        TrackerHitOutputRelations = hit_relation_collection(prefix) + "Coned",
        Dist3DCut = 30.0,
        DeltaRCut = -1.0,
        FillHistograms = False,
        OutputLevel = INFO,
    )


def tracker_coner_cfgs(args):
    """Return one TrackerHitHelixFilter per tracker subdetector."""
    return [_coner_cfg(prefix, sim) for prefix, sim in TRACKER_SUBDETECTORS]
