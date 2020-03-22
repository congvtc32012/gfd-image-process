# -*- coding: utf-8 -*-
# Author :  Hengsheng ZHAO

import easygui as gui
import imghdr
import math
import os
from math import pi

import cv2 as cv


# selected the database of the shape of image
def Init():
    # Variables initialization
    path = gui.diropenbox("A", "B")
    files = os.listdir(path)
    if path is not None:  # If we didn't click in the cancel bottom
        rad = gui.integerbox("Enter radian", "int ", 10, 1, 20)
        ang = gui.integerbox("Enter angle", "int ", 10, 1, 20)
        for file in files:  # parcourir fichier  #O(n)
            fic = path + '/' + file
            if os.path.isdir(fic):  # If the file selected is a directory
                continue
            else:
                if imghdr.what(fic) is None:  # Check if the picture is not a picture
                    continue
                else:  # if the file is not a directory and a picture
                    img = cv.imread(fic)  # read the picture with cv.imread()
                    grayScale = cv.cvtColor(img, cv.COLOR_RGB2GRAY)  # calculate
                    grayScale -= 255
                    sp = img.shape

                    OutputFeatureVectorFD(sp, grayScale, rad, ang)
    else:
        print("User has canceled the operation")


# Return the centroid of the shape of image
def CalculCentroid(sp, grayScale):  # 2,3 of Algorithm of deriving GFD
    # input:shape of the picture, Gray Scale of the Picture, rad and ang entered by the user
    # output: localisation of the centroid (xc,yc)

    # Variable Initialization
    xc = 0
    yc = 0
    pixelSum = 1

    for i in range(0, sp[1]):
        for j in range(0, sp[0]):
            a = grayScale[j, i]
            if a == 255:
                xc += j
                yc += i
                pixelSum += 1
    xc = (xc // pixelSum)
    yc = (yc // pixelSum)
    centroid = (xc, yc)

    return centroid


# Return the max Radius of the shape
def GetMaxRadius(sp, grayScale):  # Get the maximum radius of the shape image (maxRad);
    # input:shape of the picture, Gray Scale of the Picture, rad and ang entered by the user    
    # output: Max radius of the shape

    # Variable initialization
    distance = 0
    distanceInit = 0
    xc, yc = CalculCentroid(sp, grayScale)
    # Algorithm
    for i in range(0, sp[1]):  # height
        for j in range(0, sp[0]):
            if grayScale[j, i] == 0:
                distanceInit = math.sqrt((pow((j - xc), 2)) + (pow((i - yc), 2)))
            if distanceInit > distance:
                distance = distanceInit

    maxrad = (xc, yc)
    return maxrad, distance


# calculate the Polar Fourier Transform
def PolarFourierTransform(sp, grayScale, m, n):
    # input:shape of the picture, Gray Scale of the Picture, rad and ang entered by the user
    # output: real part of spectra FR[] & imaginary part of spectra FI[]

    # Variable initialization
    (xc, yc), distance = GetMaxRadius(sp, grayScale)
    FR = [[0 for j in range(0, n)] for i in range(0, m)]  # define the
    FI = [[0 for j in range(0, n)] for i in range(0, m)]
    # Algorithm
    for rad in range(m):
        # For radial frequency (rad) from zero to maximum radial frequency (m)
        for ang in range(n):
            # For angular frequency (ang) from zero to maximum angular frequency (n)
            for x in range(0, sp[1]):
                # For x from zero to width of the shape image
                for y in range(0, sp[0]):
                    # For y from zero to height of the shape image {
                    radius = math.sqrt(pow(x - xc, 2) + pow(y - yc, 2))
                    # radius = square root[(x-maxRad)2 + (y-maxRad)2];
                    theta = math.atan2((y - yc), (x - xc))
                    # theta = arctan2[(y-maxRad)/(x-maxRad)]; theta falls within [–π, +π]
                    if theta < 0:
                        theta += 2 * math.pi
                        # extend theta to [0, 2π[
                    FR[rad][ang] += (
                            grayScale[y, x] * math.cos((2 * pi) * rad * (radius / distance) + (ang * theta))
                    )
                    # FR[rad][ang] += f(x,y)×cos[2π×rad×(radius/maxRad) + ang×theta]; /* real part of spectra */
                    FI[rad][ang] -= (
                            grayScale[y, x] * math.sin((2 * pi) * rad * (radius / distance) + ang * theta)
                    )
                    # FI[rad][ang] −= f(x,y) ×sin[2π×rad×(radius/maxRad) + ang×theta]; /* imaginary part of spectra */

    return FR, FI, distance
    # For angular frequency (ang) from zero to maximum angular frequency (n)


def CalculateFD(sp, grayScale, m, n):
    # input:shape of the picture, Gray Scale of the Picture, rad and ang entered by the user
    # output: GFD[]

    global DC
    GFD = [0 for i in range(0, m * n)]
    FR, FI, dist = PolarFourierTransform(sp, grayScale, m, n)

    for rad in range(m):  # For rad from one to m
        for ang in range(n):  # For ang from one to n
            if rad == 0 and ang == 0:
                pow2FR = pow(FR[0][0], 2)
                DC = math.sqrt((pow2FR + pow2FR))
                GFD[0] = DC / (pi * pow(dist, 2))  # FD[0] = square root[(FR^2[0][0] + FR2[0][0]) / (
                # π×maxRad^2)];

            else:
                pow2FR = pow(FR[rad][ang], 2)
                pow2FI = pow(FI[rad][ang], 2)
                s = (rad * n) + ang
                GFD[s] = math.sqrt((pow2FR + pow2FI)) / DC  # FD[rad×n + ang] = squareroot[(FR2[rad][ang] + FI^2[rad][
                # ang]) / FD[0]];

    return GFD


def OutputFeatureVectorFD(sp, grayScale, m, n):
    # input:shape of the picture, Gray Scale of the Picture, rad and ang entered by the user
    # output: file type .gfd
    GFD = CalculateFD(sp, grayScale, m, n)
    for rad in range(m):  # For rad from one to m
        for ang in range(n):  # For ang from one to n
            print(GFD[rad * m + ang])


Init()
