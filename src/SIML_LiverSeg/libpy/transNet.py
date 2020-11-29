import numpy as np
import matplotlib.pyplot as plt
from skimage import transform, morphology
from scipy import ndimage
import SimpleITK as sitk

def bwVolFilter (binvol):
    binimg = sitk.GetImageFromArray(binvol.astype(np.int32))
    cc = sitk.ConnectedComponent(binimg)
    stats = sitk.LabelIntensityStatisticsImageFilter()
    stats.Execute(cc, binimg)
    tempVol = 0
    bigLabel = 0
    for l in stats.GetLabels():
        if stats.GetNumberOfPixels(l) > tempVol:
            tempVol = stats.GetNumberOfPixels(l)
            bigLabel = l
    return sitk.GetArrayFromImage(cc == bigLabel)

def bioNumpyToVnet(inputArray):
    inputArray = np.fliplr(inputArray)
    inputArray = np.rot90(inputArray, k=1, axes=(0,1))
    finalOutput = np.flip(inputArray, axis=2)
    #finalOutput = transform.resize(inputArray, [144, 144, 144])
    return finalOutput

def rmStomachSpleen(dataArray, labelArray):
    dataArray[labelArray == 1] = -1000
    dataArray[labelArray == 6] = -1000
    return dataArray

def ascitesCorrect(inputData):
    selem = morphology.disk(2)
    for i in range(0, np.shape(inputData)[2]):
        tmpImage = inputData[:,:,i]
        tmpData = inputData[:,:,i]
        tmpImage = morphology.binary_opening((tmpImage < 15).astype(int), selem)
        label_im, nb_labels = ndimage.label(tmpImage)
        sizes = ndimage.sum(tmpImage, label_im, range(nb_labels + 1))
        mask_size = sizes < 1500
        remove_pixel = mask_size[label_im]
        tmpImage[remove_pixel] = 0
        tmpData[tmpImage] = -100
        inputData[:,:,i] = tmpData
    return inputData

def saveOri(inputData):
    selem = morphology.ball(2)
    inputData = morphology.binary_opening(inputData, selem)
    return bwVolFilter(inputData)

def postProcFinal(inputData, inputLabel):
    selem = morphology.ball(2)
    justLiver = (inputLabel > 0)
    nonLungMask = (inputData < 0)
    justLiver = np.logical_and(justLiver, np.invert(nonLungMask)).astype(int)
    justLiver = bwVolFilter(justLiver)
    for i in range(0, np.shape(inputData)[2]):
        tmpImage = inputData[:,:,i]
        label_im, nb_labels = ndimage.label(tmpImage)
        sizes = ndimage.sum(tmpImage, label_im, range(nb_labels + 1))
        mask_size = sizes < 50
        remove_pixel = mask_size[label_im]
        tmpImage[remove_pixel] = 0
        inputData[:,:,i] = tmpImage
    justLiver = morphology.binary_closing(justLiver, selem)
    justLiver = bwVolFilter(justLiver)
    return justLiver