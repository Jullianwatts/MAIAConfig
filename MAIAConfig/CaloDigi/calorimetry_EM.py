from GaudiKernel.Constants import INFO, WARNING
from Configurables import DigitiserSiliconMip, CellEnergyCalibratorSiliconMip
from Common.overlay_utils import overlay_input

def ECalBarrelDigi_cfg(args):
    """
    Create a new ECal barrel digitiser instance with the given parameters.
    """
    inputHitCollection = overlay_input("ECalBarrelCollection", args)[0]
    return DigitiserSiliconMip(
        "ECalBarrelDigi",
        calibration_mip = 0.0001575,
        threshold = 5e-05,
        thresholdUnit = "GeV",
        timingCorrectForPropagation = 1,
        timingCut = 1,
        timingResolution = 0.0,
        timingWindowMax = 1.0,
        timingWindowMin = -0.5,
        elec_range_mip = 15000.0,
        CaloType = "em", CaloID = "ecal", CaloLayout = "barrel",
        inputHitCollection = inputHitCollection,
        inputHeaderCollection = "EventHeader",
        outputHitCollection = "EcalBarrelCollectionDigi",
        outputRelationCollection = "EcalBarrelRelationsSimDigi",
        OutputLevel = INFO
    )

def ECalBarrelReco_cfg():
    """
    Create a new ECal barrel reco instance with the given parameters.
    """
    return CellEnergyCalibratorSiliconMip(
        "ECalBarrelReco",
        calibration_factorsMipGev = [0.00641222630095],
        calibration_layergroups = [50],
        inputLinkCollection = "EcalBarrelRelationsSimDigi",
        outputHitCollection = "EcalBarrelCollectionRec",
        outputRelationCollection = "EcalBarrelRelationsSimRec",
        OutputLevel = INFO
    )

def ECalEndcapDigi_cfg(args):
    """
    Create a new ECal endcap digitiser instance with the given parameters.
    """
    inputHitCollection = overlay_input("ECalEndcapCollection", args)[0]
    return DigitiserSiliconMip(
        "ECalEndcapDigi",
        calibration_mip = 0.0001575,
        threshold = 5e-05,
        thresholdUnit = "GeV",
        timingCorrectForPropagation = 1,
        timingCut = 1,
        timingResolution = 0.0,
        timingWindowMax = 1.0,
        timingWindowMin = -0.5,
        elec_range_mip = 15000.0,
        CaloType = "em", CaloID = "ecal", CaloLayout = "endcap",
        inputHitCollection = inputHitCollection,
        inputHeaderCollection = "EventHeader",
        outputHitCollection = "EcalEndcapCollectionDigi",
        outputRelationCollection = "EcalEndcapRelationsSimDigi",
        OutputLevel = INFO
    )

def ECalEndcapReco_cfg():
    """
    Create a new ECal endcap reco instance with the given parameters.
    """
    return CellEnergyCalibratorSiliconMip(
        "ECalEndcapReco",
        calibration_factorsMipGev = [0.00641222630095],
        calibration_layergroups = [50],
        inputLinkCollection = "EcalEndcapRelationsSimDigi",
        outputHitCollection = "EcalEndcapCollectionRec",
        outputRelationCollection = "EcalEndcapRelationsSimRec",
        OutputLevel = INFO
    )
