import pandas as pd
import amaazetools.dicom as dicom

df = pd.read_csv('ScanLayout.csv')
scanlayout = df[['CT','ScanPacket','CTHead2Tail','Mirrored','1','2','3','4']].copy()
chopsheet = dicom.process_dicom('DICOM', scanlayout, CTdir='ScanOverviews', Meshdir='Meshes', 
						     chopsheet=None, threshold=2000, padding=15)
chopsheet.to_csv('ChopLocations.csv', index=False)
