from Configurables import GNNTrackFinder, SortTrackerHitsAlg
from Gaudi.Configuration import VERBOSE, INFO, DEBUG

def HitSorter_cfg(args):
    """
    Create a new SortTrackerHitsAlg instance for sorting hits by radius.
    """
    return SortTrackerHitsAlg(
        "SortHitsByPhi",
        InputHitCollection=["MergedTrackerHits"],
        OutputHitCollection=["MergedTrackerHitsSortedByPhi"],
        SortBy="phi",
        Descending=False,
    )

def GNNTracker_cfg(args):
    """
    Create a new GNNTrackFinder instance for GNN tracking.
    """
    return GNNTrackFinder(
        "GNNTrackFinder",
        EdgeClassifierModelPath=[str(args.modelBase + "/edge_classifier-InteractionGNN2-v2.onnx")],
        EdgeClassifierCut=[0.01],
        NodeEmbeddingModelPath=str(
            args.modelBase + "/graph_construction-MetricLearningT-v2.onnx"
        ),
        EdgeBuildingRadius=0.1,
        # Only caps the neighbours per hit on CUDA, the CPU edge building keeps
        # all neighbours within EdgeBuildingRadius.
        EdgeBuildingKnn=100,
        EmbeddingFixedInputLength=0,
        KeepEmbeddingPadding=False,
        EdgeClassifierFixedInputLength=0,
        InputFeaturesEmbedding=["r", "phi", "z", "eta", "t"],
        InputScalesEmbedding=[1000.0, 3.14, 1000.0, 1.0, 1.0],
        InputFeaturesEdgeClassifier=[["r", "phi", "z", "eta", "t"]],
        InputScalesEdgeClassifier=[[1000.0, 3.14, 1000.0, 1.0, 1.0]],
        # Orient every edge from the hit closer to the interaction point to the
        # one further out, as the ACORN pipeline does.
        SortEdges=True,
        # InteractionGNN2 has three inputs and takes the six edge features
        # (dr, dphi, dz, deta, phislope, rphislope) as its edge_attr, so they
        # have to be computed. The scales are those of r, phi, z and eta -- in
        # that order, which is *not* the order of InputFeaturesEdgeClassifier
        # above. The classifier does not scale its edge input, so these have to
        # be the scales it was trained with. Turn both off for a two-input model.
        ComputeEdgeFeatures=True,
        EdgeFeatureScales=[1000.0, 3.14, 1000.0, 1.0],
        PhiBins=50,
        PhiOverlap=0.1,
        TrackBuilding="cc-and-walk",
        WalkAddScore=0.6,   # follow every neighbour above this, branching if several
        WalkMinScore=0.1,   # else follow only the best, and only above this
        MinHitsPerTrack=3,
        ExtrapolateToCalo=True,
        AddEndcapCaloState=True,
        # "cpu" or "cuda" (optionally "cuda:<index>"). The default image ships a
        # CPU-only onnxruntime, so "cuda" requires a CUDA-enabled build.
        Device=getattr(args, "device", "cpu"),
        OutputLevel=DEBUG,
        DetailedDebugOut=False, # If True this will print all inputs in full detail!
        InputHitCollections=[
            "MergedTrackerHitsSortedByPhi",
        ],
        OutputTrackCandidates=["GNNTrackCandidates"],
    )
