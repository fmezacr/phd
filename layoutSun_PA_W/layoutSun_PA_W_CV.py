
import cv2 as cv
import numpy as np
import math
import glob
import os


# The function generateSunLayout() generates an image of the sun's layout,
# taking as parameters the resolution of the image, the radius and center of the
# generated circle, the vector PA and the width W.

def generateSunLayout(imgResolution, cirCenter, r, PA, W):
    # Matrix of size imgResolution (px,px) filled with 1's. That matrix represents
    # the white background of the generated image.
    img = np.ones((imgResolution[0], imgResolution[1], 3), np.uint8) * 255

    # Circle with center in the cirCenter point. The function
    # cv.circle() receives the desired radius (r) of the circle as a parameter
    cv.circle(img, cirCenter, r, (255,0,0), 2, cv.LINE_AA)


    # x_PA , y_PA are the variables that locate the vector PA in the circle.
    x_PA = int(r * 1.1 * math.cos(3*math.pi/2 - PA*math.pi/180)) + cirCenter[0]
    y_PA = int(r * 1.1 * math.sin(3*math.pi/2 - PA*math.pi/180)) + cirCenter[1]

    # vector PA
    cv.arrowedLine(img, cirCenter, (x_PA, y_PA), (0,0,255), 2, tipLength = 0.05)

    # (x_upW, y_upW) and (x_downW, y_downW) locate W
    x_upW = int(r*1.1*math.cos((3*math.pi/2 - PA*math.pi/180) + W*math.pi/360)) + cirCenter[0]
    y_upW = int(r*1.1*math.sin(3*math.pi/2 - PA*math.pi/180 + W*math.pi/360)) + cirCenter[1]

    x_downW = int(r*1.1*math.cos((3*math.pi/2 - PA*math.pi/180) - W*math.pi/360)) + cirCenter[0]
    y_downW = int(r*1.1*math.sin(3*math.pi/2 - PA*math.pi/180 - W*math.pi/360)) + cirCenter[1]

    # lines that limits W area
    cv.line(img, cirCenter, (x_upW, y_upW), (0,0,0), 2, cv.LINE_AA)
    cv.line(img, cirCenter, (x_downW, y_downW), (0,0,0), 2, cv.LINE_AA)

    # the generated image is returned
    return img

# Overlaps the orinal and generated images. Return the overlaped image
def overlayImageSun_GeneratedSunLayout(pathSunImage, generatedSunLayout):
    sunImage = cv.imread(pathSunImage)
    outputImage = cv.addWeighted(generatedSunLayout, 0.3, sunImage, 1-0.3, 0, sunImage)
    #cv.imshow("sun", sunImage)
    #cv.imwrite('sun.jpg', sunImage)
    return outputImage

# Counts the number of images in a directory and return a result directory
# with the overlaped images
def analizeDirSunImage(pathDirProyect):
    imgResolution = (1024, 1024)
    cirCenter = (512, 512)
    r = 380
    PA = 50
    W = 80

    # Determines the number of images in the project directory
    numElements = len(glob.glob(pathDirProyect+"*.jpg"))

    # Create the results directory
    if not os.path.exists("dirResult"):
        os.makedirs("dirResult")

    # It iterates over the images, extracting the parameters
    # and generating the layout of each FITS image
    for i in range(0, numElements):
        path = pathDirProyect+str(i)+".jpg"
        outName = "dirResult/"+"result"+str(i)+".jpg"

        # Se abren y extraen los datos de la imagen FITS
        # function extractParameters() *** PENDIENTE ****
        image = generateSunLayout(imgResolution, cirCenter, r, PA, W)
        out = overlayImageSun_GeneratedSunLayout(path, image)

        cv.imwrite(outName, out)

# The main() function
def main():

    imgResolution = (1024, 1024)
    cirCenter = (512, 512)
    r = 380
    PA = 50
    W = 80

    analizeDirSunImage("SunX/")


if __name__ == '__main__':
    main()
