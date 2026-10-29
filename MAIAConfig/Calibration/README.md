# Pandora theta-energy calibration tables

Used only with `--pandoraCalibration default` (off by default).

- `ecal_theta_energy_calib.json`: EM branch, trained on single photons
- `hadronic_theta_energy_calib.json`: hadronic branch, trained on single pions

Produced with pandora-calibration-tools
(`make_ecal_theta_energy_calibration.py`, `make_hcal_theta_energy_calibration.py`)
from v2.11 (Marlin) reconstruction, with ECalToEM = 1.02373335516,
ECalToHad = 1.38, HCalToHad = 1.25 and software compensation off. The
calibration switches Pandora to these values when enabled; see
`Common/pandora_calibration.py`.

Outside the table range the correction is 1.0: EM clusters below 30 GeV and
hadronic clusters below 10 GeV are not corrected.
