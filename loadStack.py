
# Takes a render stack and a z-value for a section and reads in all the parameters required for locating tiles location in the downsampled images

import os, sys, json
import urllib
import matplotlib.pyplot as plt
import matplotlib.path as mplpath
import numpy as np
import cv2, PIL
from imageCanvas import *


def loadTileSpecs(stack,z):
    # stack - a structure that contains the baseUrl, owner, project, stackname, etc.
    # z - z-value of the section

    # get a list of all tiles
    urlChar = stack["baseUrl"] + '/owner/' + stack["owner"] + '/project/' + stack["project"] + '/stack/' + stack["stackname"] + '/z/' + str(z) + '.0' + '/tile-specs'
    f = urllib.urlopen(urlChar)
    data = json.loads(f.read())
    return data

def loadTileData(stackJsonData,stack):
    tileData = {}
    for i,jt in enumerate(stackJsonData):
        td = {}
        td["z"] = jt["z"]
        td["id"] = i
        td["tileId"] = jt["tileId"]
        td["height"] = jt["height"]
        td["width"] = jt["width"]
        td["minX"] = jt["minX"]
        td["minY"] = jt["minY"]
        td["maxX"] = jt["maxX"]
        td["maxY"] = jt["maxY"]
        sectionId = jt["layout"]["sectionId"]

        #compute tile centers in world coordinates
        td["centerX"] = (td["maxX"]-td["minX"])/2
        td["centerY"] = (td["maxY"]-td["minY"])/2

        # Not used at the moment
        #td["camera"] = jt["layout"]["camera"]
        #td["stageX"] = jt["layout"]["stageX"]
        #td["stageY"] = jt["layout"]["stageY"]
        #td["imageRow"] = jt["layout"]["imageRow"]
        #td["imageCol"] = jt["layout"]["imageCol"]
        #td["owner"] = stack["owner"]
        #td["project"] = stack["project"]
        #td["stackname"] = stack["stackname"]
        tileData[sectionId] = td
    return tileData

def selectTilesInsidePolygon(polygonPoints,tileData):
    # polygonPoints is a set of coordinates that define the polygon boundary
    # note that the first and last coordinates are not the same in polygonPoints
    # returns a set of tile indices referencing tileData indices for those tiles whose centers are within the polygon

    # extract the tile center from tileData
    tileCenters = []
    tileIds = []
    for td in tileData:
        tileCenters.append([td["centerX"], td["centerY"]])
        tileIds.append(td["tileId"])

    # create a bounding box path for the polygon
    pPoints = np.array(polygonPoints)
    bbpath = mplpath.Path(pPoints)

    # check if the tile centers are within the polygon
    contains = bbpath.contains_points(tileCenters)

    # extract the indices of those tiles whose centers are within the polygon
    indices = np.nonzero(contains==True)[0]

    # extract the tile IDs from the indices
    tileId = []
    for i in indices:
        tileId.append(tileIds[i])
    return tileId


if __name__ == '__main__':
    stack = {}
    stack["baseUrl"] = "http://em-131fs:8080/render-ws/v1"
    stack["owner"] = "gayathri"
    stack["project"] = "EM_Phase1"
    stack["stackname"] = "Phase1RawData_AIBS"
    downsampledImgPath = "/data/em-131fs/gayathri/downsampledSections"
    ext = "jpg"
    z = 2267

    tileSpecs = loadTileSpecs(stack,z)
    #print tileSpecs[0]

    # get section ID
    sectionId = tileSpecs[0]["layout"]["sectionId"]
    #print sectionId

    # get the bounds of all tiles in this section
    tileData = loadTileData(tileSpecs,stack)
    #print tileData[sectionId]

    # Read the downscaled image of each section
    files = os.listdir(downsampledImgPath)

    for f in files:
        f = os.path.join(downsampledImgPath, f)
        if (os.path.isfile(f) and f.endswith(ext)):
            section = f[len(downsampledImgPath)+1:-3] + '0'
            section = "2267.0"

            # read the down sampled image
            #img = cv2.imread(f)
            #img_width = img.shape[1]
            #img_height = img.shape[0]

            # compute width and height of the bounds of the section
            #bounds_width = bounds['maxX']-bounds['minX']
            #bounds_height = bounds['maxY']-bounds['minY']

            # compute the scale between the original size and the downsampled image
            #scale = img_width*1.0/bounds_width

            bounds = {}
            bounds["minX"] = tileData[section]['minX']
            bounds["minY"] = tileData[section]['minY']
            bounds["maxX"] = tileData[section]['maxX']
            bounds["maxY"] = tileData[section]['maxY']

            # set up the image canvas to show the downscaled image and get the polgon roi
            canvasImage = imageCanvas(f)

            # show the image and collect the polygon points. The polygon points are saved in the canvas object
            #canvasImage.getCoord()
            canvasImage.showImage()
            print len(canvasImage.polygon)
