import pandas as pd
import amaazetools.dicom as dicom


#Refine the initial dicom processing, if necessary
df = pd.read_csv('ScanLayout.csv')
scanlayout = df[['CT','ScanPacket','CTHead2Tail','Mirrored','1','2','3','4']].copy()
chopsheet = pd.read_csv('ChopLocations.csv')
dicom.process_dicom('DICOM', scanlayout, chopsheet=chopsheet)
