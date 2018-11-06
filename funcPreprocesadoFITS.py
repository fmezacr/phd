from sunpy.net import Fido, attrs as a
from sunpy.time import TimeRange, parse_time
from sunpy.timeseries import TimeSeries
import astropy.units as u
import cv2 as cv
import numpy as np
import math
import glob
import os
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from skimage.feature import peak_local_max
from astropy.io import fits
import sunpy.map
from sunpy.data.sample import AIA_193_IMAGE

# Funcion que retorna un intervalo de fechas correspondiente
# a una fecha central +/- un delta en minutos.
# Es decir (centralDate - delta_min , centralDate + delta_min)
# El intervalo de fechas se retorna como un objeto de tipo TimeRange
def returnDataRange(centralDate, delta_min):
    date_rangeUp = TimeRange(centralDate, delta_min * u.min).previous()
    date_rangeFinal = TimeRange(date_rangeUp.start, date_rangeUp.next().end)
    return date_rangeFinal

def peakLocalMax(aiaMapData, pixDist, threshold):
    peakCoordinates = peak_local_max(aiaMapData, min_distance= pixDist, threshold_rel= threshold)
    return peakCoordinates


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
    fits_image_filename = '/home/yasser/Documents/DatosJupyterSun/JSOC_AIA_FITS/aia.lev1_euv_12s.2011-06-07T070133Z.193.image_lev1.fits'
    sunImageFile = fits.open(fits_image_filename)

#    goesFits = fits.open('go1520110607.fits')
#    print(goesFits)

    # Se muestra el disco solar usando la libreria sunpy
    aiamap = sunpy.map.Map(fits_image_filename)
    aiamapSample = sunpy.map.Map(AIA_193_IMAGE)


    peakCoord = peakLocalMax(aiamapSample.data, 60, 0.5)
    print peakCoord

    plt.figure()
    aiamap.plot()
    plt.show()

    # Se obtiene e imprime el centro y radio del sol
    centroSol = centerSunFITSVariables(sunImageFile[1])
    radioSol = getSunRadious(sunImageFile[1])
    print centroSol
    print radioSol

    # Pruebas funcion returnDataRange
    fechaC1 = '2018/06/26 07:40'
    delta1 = 20
    fechaC2 = '2010/03/04 00:00'
    delta2 = 10

    inter1 = returnDataRange(fechaC1, delta1)
    inter2 = returnDataRange(fechaC2, delta2)

    print(inter1)
    print(inter2)

#    print(sunImageFile[1].header)
#    imageSunData = getHDUListData(sunImageFile[1])
#    print imageSunData
#    imSunROI= drawROI(imageSunData, centroSol, radioSol, 1)
#    cv.imwrite("ImageSunOut.png", imSunROI)
#    sunImageRead5 = cv.imread("ImageSunOut.png", -1)

    sunImageFile.close()    # Funcion de astropy para cerrar FITS y liberar memoria
#    goesFits.close()
if __name__ == '__main__':
    main()
