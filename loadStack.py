
# Takes a render stack and a z-value for a section and reads in all the parameters required for locating tiles location in the downsampled images

import os, sys, json
import urllib
import matplotlib.pyplot as plt
import matplotlib.path as mplpath
import numpy as np
import cv2, PIL
from imageCanvas import *
from stackPointConversion import stackPointConversion


if __name__ == '__main__':
    stack = {}
    stack["baseUrl"] = "http://em-131fs:8080/render-ws/v1"
    stack["owner"] = "gayathri"
    stack["project"] = "EM_Phase1"
    stack["stackname"] = "Phase1RawData_AIBS"
    downsampledImgPath = "/data/em-131fs/gayathri/downsampledSections"
    ext = "jpg"
    z = 2267

    sp = stackPointConversion()

    # Read the downscaled image of each section
    files = os.listdir(downsampledImgPath)
    for f in files:
        f = os.path.join(downsampledImgPath,f)
        if (os.path.isfile(f) and f.endswith(ext)):
            # assumes that the downsampled images are named after their z value
            z = int(f[len(downsampledImgPath)+1:-4])
            sectionId = str(z) + '.0'
            print sectionId

            # this is required to reupload sections with only selected tiles
            tileSpecs = sp.getTileSpecs(stack,z)
            #print tileSpecs[0]

            # get section bounds
            secBounds = sp.getSectionBounds(stack,z)

            # get section ID
            sectionId = tileSpecs[0]["layout"]["sectionId"]
            #print sectionId

            # get the bounds of all tiles in this section
            tileBounds = sp.getTileBounds(stack, z)

            # set up the image canvas to show the downscaled image and get the polygon roi
            canvasImage = imageCanvas(f)

            # show the image to get some polygons on it
            canvasImage.showImage()

            # convert the polygon points to world coordinates using section bounds
            canvasImage.convertPolygonPointsToWorld(secBounds)

            # find the tiles whose center falls within this polygon
            print canvasImage.polygon[0].worldCoords
            tileIDs = sp.selectTilesInsidePolygon(canvasImage.polygon[0].worldCoords, tileBounds)
            print tileIDs


#    for f in files:
#        f = os.path.join(downsampledImgPath, f)
#        if (os.path.isfile(f) and f.endswith(ext)):
#            section = f[len(downsampledImgPath)+1:-3] + '0'
#            section = "2267.0"
#
#            # read the down sampled image
#            #img = cv2.imread(f)
#            #img_width = img.shape[1]
#            #img_height = img.shape[0]
#
#            # compute width and height of the bounds of the section
#            #bounds_width = bounds['maxX']-bounds['minX']
#            #bounds_height = bounds['maxY']-bounds['minY']
#
#            # compute the scale between the original size and the downsampled image
#            #scale = img_width*1.0/bounds_width
#
#            tileBounds = {}
#            tileBounds["minX"] = tileData[section]['minX']
#            tileBounds["minY"] = tileData[section]['minY']
#            tileBounds["maxX"] = tileData[section]['maxX']
#            tileBounds["maxY"] = tileData[section]['maxY']
#
#            # set up the image canvas to show the downscaled image and get the polgon roi
#            canvasImage = imageCanvas(f)
#
#            # show the image and collect the polygon points. The polygon points are saved in the canvas object
#            #canvasImage.getCoord()
#            canvasImage.showImage()
#            print len(canvasImage.polygon[0].coords)
