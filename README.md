# CT-Surfacing

This repository gives an example of how to surface (i.e., create 3D models from) CT images containing multiple objects. The code requires the [AMAAZETools](https://github.com/jwcalder/AMAAZETools) package. To illustrate how the code works, we have included in this repository CT data from 2 scans in the DICOM folder. The ScanOverviews folder shows images of the scans from the top and side of the scanning bed. Each scan has 4 bone fragments. The code in this repository creates all the data in the ScanOverviews and Meshes folder from the DICOM data.

The code requires a layout spreadsheet provided by the user. Here, we use the file `ScanLayout.csv`. Each row of the spreadsheet corresponds to a CT scan. The spreadsheet must have the columns `CT`, `ScanPacket`, `CTHead2Tail`, and `Mirrored`, in that order, followed by one column for each object in the CT scan. The `CT` column is a scan-date identifier string; the `ScanPacket` column identifies the name of the subfolder in `DICOM` containing the CT data; the column `CTHead2Tail` indicates if the object names that follow should be read left-to-right, or right-to-left in the scan, and should contain either `L2R` or `R2L`; finally, the `Mirrored` column indicates if the CT image is mirrored along the direction of the scanning bed, and should be `yes` or `no` (most often `no` is correct). 

The code requires `pandas` and `amaazetools.dicom`, which are first loaded with the commands.
```
import pandas as pd
import amaazetools.dicom as dicom
```

Given a properly formated `ScanLayout.csv` file, the first step is to separate the objects within each CT scan. The code below performs an initial pass, attempting to do this automatically. This code is also in the script `dicom_firstpass.py`.
```
df = pd.read_csv('ScanLayout.csv')
scanlayout = df[['CT','ScanPacket','CTHead2Tail','Mirrored','1','2','3','4']].copy()
chopsheet = dicom.process_dicom('DICOM', scanlayout, CTdir='ScanOverviews', Meshdir='Meshes', chopsheet=None, threshold=2000, padding=15)
chopsheet.to_csv('ChopLocations.csv', index=False)
```
The code attempts to automatically detect the objects in the CT scan, and saves overviews of the CT scan with bounding boxes around each object in the `CTdir` folder (here, `ScanOverviews`), and saves individual projected images of each object to the `Meshdir` (here, `Meshes`). The coordinates of the bounding boxes of each object are saved to the .csv file `ChopLocations.csv`, and they can be edited by hand, if necessary (see below).

If all the objects are detected properly, then we can proceed to surface the bones with the code below (also in `surface.py`).
```
dicom.surface_bones('Meshes', iso=2500, write_gif=False)
```
The first argument is the directory `Meshdir` from the first pass code above. The `iso` value is the threshold for surfacing the CT images, and `write_gif` controls whether to save a rotating .gif of the object. This requires the [Mayavi](https://docs.enthought.com/mayavi/mayavi/) package, which can be difficult to install. This code creates .ply files for each object and saves them in the `Meshes` folder. 

Now, if the initial run of `dicom.process_dicom` does not detect the object properly, then some fine-tuning can be done by manually editing the `ChopLocations.csv` file and re-running `dicom.process_dicom`, this time providing the new, edited, chopsheet. The .csv file `ChopLocations.csv` contains a column `Process` that can be used to process only scans that were incorrectly chopped up, which can save time. The other columns give the starting and ending coordinates of the bounding box of each object in all three coordinate directions. After editing the .csv file, the code below runs `process_dicom` with the edited `ChopLocations.csv` file. This code is contained in `dicom_refine.py` as well.

```
df = pd.read_csv('ScanLayout.csv')
scanlayout = df[['CT','ScanPacket','CTHead2Tail','Mirrored','1','2','3','4']].copy()
chopsheet = pd.read_csv('ChopLocations.csv')
dicom.process_dicom('DICOM', scanlayout, CTdir='ScanOverviews', Meshdir='Meshes', chopsheet=cropsheet, threshold=2000, padding=15)
```
This will create new .png files in `Meshes` and `ScanOverviews`. It may take several iterations to get the bounding boxes in the correct location. Other parameters that can be adjusted are the `threshold=2000` and `padding=15`. The threshold is used to detect the objects and specific to bone in CT images. The padding refers to the number of pixels to add to the detected object on each side when creating the bounding box.

