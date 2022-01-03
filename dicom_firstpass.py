import pandas as pd
import amaazetools.dicom as dicom


#Initial processing
df = pd.read_csv('ScanLayout.csv')
scanlayout = df[['CT','ScanPacket','CTHead2Tail','Mirrored','1','2','3','4']].copy()
chopsheet = dicom.process_dicom('DICOM', scanlayout)
chopsheet.to_csv('ChopLocations.csv', index=False)
