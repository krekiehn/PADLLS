# Import libraries
import sys
import os
import glob
from libpy.allToNumpy import dcmToNumpy
from libpy.transNet import bioNumpyToVnet, rmStomachSpleen, ascitesCorrect, saveOri, postProcFinal
import matplotlib.pyplot as plt
import nibabel as nib 
from natsort import natsorted
print('Imported libraries')
# Create constants
DCM_DATA_INPUT = './data/dcmData/*'
VNET_DATA_INPUT = './lib/vnet/data/dense_vnet_abdominal_ct/'
VNET_CONFIG = './lib/vnet/extensions/dense_vnet_abdominal_ct/config.ini'
VNET_DATA_OUTPUT = './lib/vnet/models/dense_vnet_abdominal_ct/segmentation_output/*.nii.gz'
NII_HEADER_FILE = './data/100_CT.nii'
HNET_DATA_INPUT = './data/hnetInputData/'
HNET_ORI_INPUT = './data/livermask/'
HNET_DATA_OUTPUT = './data/hnetResults/'
FINAL_OUTPUT = './output/'
print('Created constants')
# Create vnet input data
# tmpHeadImage = nib.load(NII_HEADER_FILE)
# folderNames = natsorted(glob.glob(DCM_DATA_INPUT))
# index = 0
# for folder in folderNames:
#     dcmArray = dcmToNumpy(folder)
#     procArray = bioNumpyToVnet(dcmArray)
#     niiImage = nib.Nifti1Image(procArray, tmpHeadImage.affine, tmpHeadImage.header)
#     nib.save(niiImage, VNET_DATA_INPUT + 'test-volume-' + str(index))
#     print('Saved test-volume-' + str(index))
#     index = index + 1
print('Created Vnet input data')
# Run vnet
os.system('net_segment inference -c ' + VNET_CONFIG)
print('Vnet was successfully run!')
# Create hnet input data
folderNames = glob.glob(VNET_DATA_OUTPUT)
dataFolderNames = glob.glob(VNET_DATA_INPUT + '*.nii')
folderNames = natsorted(folderNames)
dataFolderNames = natsorted(dataFolderNames)
index = 0
for folder, dataFolder in zip(folderNames, dataFolderNames):
    labelNii = nib.load(folder)
    labelArray = labelNii.get_data()
    dataNii = nib.load(dataFolder)
    dataArray = dataNii.get_data()
    dataArray = rmStomachSpleen(dataArray, labelArray)
    dataArray = ascitesCorrect(dataArray)
    labelArray = saveOri((labelArray == 5).astype(int))
    niiDataImage = nib.Nifti1Image(dataArray, None)
    nib.save(niiDataImage, HNET_DATA_INPUT + 'test-volume-' + str(index) + '.nii')
    niiLabelImage = nib.Nifti1Image(labelArray, None)
    nib.save(niiLabelImage, HNET_ORI_INPUT + str(index) + '-ori.nii')
    print('Saved test-volume-' + str(index))
    index = index + 1
print('Hnet data was created')
# Run hnet
#plt.figure()
#plt.imshow(asdfArr[:,:,110], cmap=plt.cm.gray)
#plt.show()
#os.system('cd ~ && source ./venv/bin/activate && cd ./LiverSegPy/src/ && python ./SIML_LiverSeg/lib/hnet/test.py')
os.system('cd ~ && . ./venv/bin/activate && python ./SIML_LiverSeg/lib/hnet/test.py')
print('Hnet was successfully run!')
# Process Hnet data
folderNames = natsorted(glob.glob(HNET_DATA_OUTPUT + '*.nii'))
dataFolderNames = natsorted(glob.glob(HNET_DATA_INPUT + '*.nii'))
index = 0
for folder, dataFolder in zip(folderNames, dataFolderNames):
    labelNii = nib.load(folder)
    labelArray = labelNii.get_data()
    dataNii = nib.load(dataFolder)
    dataArray = dataNii.get_data()
    justLiverMask = postProcFinal(dataArray, labelArray)
    niiLabelImage = nib.Nifti1Image(justLiverMask, None)
    nib.save(niiLabelImage, FINAL_OUTPUT + 'test-segmentation-' + str(index) + '.nii')
    print('Saved final test-volume-' + str(index))
    index = index + 1