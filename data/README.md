# data
The MoVi data set is stored here. Also, scripts regarding data preparation is also in this folder.

## Archives Extraction
Extract archives in these locations:
* `F_AMASS.tar/AMASS/*` -> [`AMASS/`](AMASS)
* `Camera Parameters.tar/Calib/*` -> [`Calib/`](Calib)
* `F_Subjects_1_45.tar/F_Subjects_1_45/*` -> [`V3D/`](V3D)
* `F_Subjects_46_90.tar/F_Subjects_46_90/*` -> [`V3D/`](V3D)
* `F_PG#_Subject_#_L.avi` -> [`Videos/`](Videos)

## Folders Structure
Folders structure:
* [`AMASS/`](AMASS) contains the full marker set MoCap augmented with 3D joints’ positions and metadata.
* [`Calib/`](Calib) contains the camera parameters (rotation matrix and translation vector).
* [`V3D/`](V3D) contains the MoCap data processed by V3D and augmented with meta-data.
* [`Videos/`](Videos) contains `.avi` videos.

## Usage
```
usage: prepare_dataset.py [-h] [--amass AMASS] [--videos VIDEOS] [--v3d V3D] [--output OUTPUT]

optional arguments:
  -h, --help       show this help message and exit
  --amass AMASS    Path to the AMASS folder.
  --videos VIDEOS  Path to the video folder.
  --v3d V3D        Path to the V3D folder.
  --output OUTPUT  Path to the the output of the prepared dataset..
```
