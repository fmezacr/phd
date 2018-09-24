import cv2 as cv
import numpy as np
import math
import glob
import os
import matplotlib.pyplot as plt
from astropy.io import fits


def centerSunFITSVariables(sunImageHDU):
    crpix1 = int(sunImageHDU.header['CRPIX1'])
    crpix2 = int(sunImageHDU.header['CRPIX2'])
    sunCenter = np.array([crpix1, crpix2])
    return sunCenter


def getHDUListData(sunImageHDU):
    data = sunImageHDU.data
    return data


def drawROI(sunImageData, sunCenter, pixRadius, proportion):
    propRadius = int(proportion * pixRadius)
    cv.rectangle(sunImageData, (sunCenter[0] - propRadius, sunCenter[1] - propRadius), (sunCenter[0] + propRadius, sunCenter[1] + propRadius), (255, 255, 255), 2)
#    cv.circle(sunImageData, (sunCenter[0], sunCenter[1]), propRadius, (255,255,255), 2, cv.LINE_AA)
    return sunImageData

def extractROI(sunImageData, sunCenter, pixRadius, proportion):
    propRadius = int(proportion * pixRadius)
    roi = sunImageData[sunCenter[1]-propRadius:sunCenter[1]+propRadius, sunCenter[0]-propRadius:sunCenter[0]+propRadius]
    return roi

# The main() function
def main():
    fits_image_filename = 'ImagenesFITS/aia.lev1_euv_12s.2012-02-07T032009Z.193.image_lev1.fits'
    sunImageFile = fits.open(fits_image_filename)

    sunImageFile.verify('fix')

    centroSol = centerSunFITSVariables(sunImageFile[1])
    print centroSol

    imageSunData = getHDUListData(sunImageFile[1])
    print imageSunData

    plt.figure()
    fig = plt.imshow(imageSunData)
    plt.show()

    cv.imwrite("ImageSunOut.png", imageSunData)

    sunImageRead5 = cv.imread("ImageSunOut.png", -1)

    print sunImageRead5

    sunImageFile.close()



if __name__ == '__main__':
    main()
