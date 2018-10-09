import cv2 as cv
import numpy as np
import math
import glob
import os
import matplotlib.pyplot as plt
from astropy.io import fits
import sunpy
import sunpy.map

# Funcion que retorna el centro del disco solar de la imagen FITS,
# las coordenadas son los tags CRPIX1 y CRPIX2 contenidos en el header.
def centerSunFITSVariables(sunImageHDU):
    crpix1 = int(sunImageHDU.header['CRPIX1'])
    crpix2 = int(sunImageHDU.header['CRPIX2'])
    sunCenter = np.array([crpix1, crpix2])
    return sunCenter

# Retorna los datos (imagen del disco solar) contenidos en archivos FTIS
def getHDUListData(sunImageHDU):
    data = sunImageHDU.data
    return data

# Devuelve el radio del disco solar en pixeles,
# usa el tag R_SUN para buscar en el header
def getSunRadious(sunImageHDU):
    rSun = int(sunImageHDU.header['R_SUN'])
    return rSun

# Dibuja sobre la imagen del disco solar una region de interes(ROI) cuadrada
# de cierta proporcion del radio
def drawROI(sunImageData, sunCenter, pixRadius, proportion):
    propRadius = int(proportion * pixRadius)
    cv.rectangle(sunImageData, (sunCenter[0] - propRadius, sunCenter[1] - propRadius), (sunCenter[0] + propRadius, sunCenter[1] + propRadius), 0, 10)
    cv.circle(sunImageData, (sunCenter[0], sunCenter[1]), propRadius, 0, 10, cv.LINE_AA)
    return sunImageData

# Funcion que extrae la ROI de la imagen del disco solar, la ROI se retorna en
# una imagen independiente
def extractROI(sunImageData, sunCenter, pixRadius, proportion):
    propRadius = int(proportion * pixRadius)
    roi = sunImageData[sunCenter[1]-propRadius:sunCenter[1]+propRadius, sunCenter[0]-propRadius:sunCenter[0]+propRadius]
    return roi

# Funcion que redimensiona los pixeles de una imagen en una escala de  0 a 255, elimina
# valores negativos sumando un offset, correspondiente al valor mas negativo en la imagen
def image255bitsTransformation(sunImageData, offset, maxData):
    newMax = maxData + offset;
    newTransfo = (sunImageData + offset) * 255/newMax

    return newTransfo

# The main() function
def main():
    # Se abre la imagen usando Astropy
    fits_image_filename = 'ImagenesFITS/aia.lev1_euv_12s.2012-02-07T032009Z.193.image_lev1.fits'
    sunImageFile = fits.open(fits_image_filename)

    sunImageFile.verify('fix')
    # Se muestra el disco solar usando la libreria sunpy
    aiamap = sunpy.map.Map(fits_image_filename)
    print aiamap
    plt.figure()
    aiamap.plot()
    plt.show()

    # Se obtiene e imprime el centro y radio del sol
    centroSol = centerSunFITSVariables(sunImageFile[1])
    radioSol = getSunRadious(sunImageFile[1])
    print centroSol
    print radioSol

#    print(sunImageFile[1].header)
#    imageSunData = getHDUListData(sunImageFile[1])
#    print imageSunData
#    imSunROI= drawROI(imageSunData, centroSol, radioSol, 1)
#    cv.imwrite("ImageSunOut.png", imSunROI)
#    sunImageRead5 = cv.imread("ImageSunOut.png", -1)

    sunImageFile.close()    # Funcion de astropy para cerrar FITS y liberar memoria

if __name__ == '__main__':
    main()
