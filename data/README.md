# data
The MoVi data set is stored here. Also, scripts regarding data preparation is also in this folder.

## Archives Extraction
Extract archives in these locations:
* `F_AMASS.tar/AMASS/*` -> `AMASS/`
* `Camera Parameters.tar/Calib/*` -> `Calib/`
* `F_Subjects_1_45.tar/F_Subjects_1_45/*` -> `V3D/`
* `F_Subjects_46_90.tar/F_Subjects_46_90/*` -> `V3D/`
* `F_PG#_Subject_#_L.avi` -> `Videos/`

# Folders Structure
Folders structure:
* `AMASS/` contains the full marker set MoCap augmented with 3D joints’ positions and metadata.
* `Calib/` contains the camera parameters (rotation matrix and translation vector).
* `V3D/` contains the MoCap data processed by V3D and augmented with meta-data.
