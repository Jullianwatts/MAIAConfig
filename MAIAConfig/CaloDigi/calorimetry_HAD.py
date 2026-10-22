from GaudiKernel.Constants import INFO, WARNING
from Configurables import DigitiserScinPpdNpe, CellEnergyCalibratorScinPpdNpe
from Common.overlay_utils import overlay_input

def HCalBarrelDigi_cfg(args):
    """
    Create a new HCal barrel digitiser instance with the given parameters.
    """
    inputHitCollection = overlay_input("HCalBarrelCollection", args)[0]
    return DigitiserScinPpdNpe(
        "HCalBarrelDigi",
        calibration_mip = 0.0004925,
        threshold = 0.5,
        thresholdUnit = "MIP",
        timingCorrectForPropagation = 1,
        timingCut = 1,
        timingResolution = 0.0,
        timingWindowMax = 10.0,
        timingWindowMin = -0.5,
        ppd_mipPe = 15.0,
        ppd_npix = 2000,
        ppd_npix_uncert = 0.0,
        ppd_pix_spread = 0.0,
        CaloType = "had", CaloID = "hcal", CaloLayout = "barrel",
        inputHitCollection = inputHitCollection,
        inputHeaderCollection = "EventHeader",
        outputHitCollection = "HcalBarrelCollectionDigi",
        outputRelationCollection = "HcalBarrelRelationsSimDigi",
        OutputLevel = INFO
    )

def HCalBarrelReco_cfg():
    """
    Create a new HCal barrel reco instance with the given parameters.
    """
    return CellEnergyCalibratorScinPpdNpe(
        "HCalBarrelReco",
        calibration_factorsMipGev = [0.0287783798145],
        calibration_layergroups = [100],
        ppd_mipPe = 15.0,
        ppd_npix = 2000,
        inputLinkCollection = "HcalBarrelRelationsSimDigi",
        outputHitCollection = "HcalBarrelCollectionRec",
        outputRelationCollection = "HcalBarrelRelationsSimRec",
        OutputLevel = INFO
    )

def HCalEndcapDigi_cfg(args):
    """
    Create a new HCal endcap digitiser instance with the given parameters.
    """
    inputHitCollection = overlay_input("HCalEndcapCollection", args)[0]
    return DigitiserScinPpdNpe(
        "HCalEndcapDigi",
        calibration_mip = 0.0004725,
        threshold = 0.5,
        thresholdUnit = "MIP",
        timingCorrectForPropagation = 1,
        timingCut = 1,
        timingResolution = 0.0,
        timingWindowMax = 10.0,
        timingWindowMin = -0.5,
        ppd_mipPe = 15.0,
        ppd_npix = 2000,
        ppd_npix_uncert = 0.0,
        ppd_pix_spread = 0.0,
        CaloType = "had", CaloID = "hcal", CaloLayout = "endcap",
        inputHitCollection = inputHitCollection,
        inputHeaderCollection = "EventHeader",
        outputHitCollection = "HcalEndcapCollectionDigi",
        outputRelationCollection = "HcalEndcapRelationsSimDigi",
        OutputLevel = INFO
    )

def HCalEndcapReco_cfg():
    """
    Create a new HCal endcap reco instance with the given parameters.
    """
    return CellEnergyCalibratorScinPpdNpe(
        "HCalEndcapReco",
        calibration_factorsMipGev = [0.0285819096797],
        calibration_layergroups = [100],
        ppd_mipPe = 15.0,
        ppd_npix = 2000,
        inputLinkCollection = "HcalEndcapRelationsSimDigi",
        outputHitCollection = "HcalEndcapCollectionRec",
        outputRelationCollection = "HcalEndcapRelationsSimRec",
        OutputLevel = INFO
    )
