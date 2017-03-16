#!/usr/bin/env python
'''
Takes a render stack and a z-value for a section and reads in all the
    parameters required for locating tiles location in the downsampled images
'''
import os
import sys
import json
import tempfile
import urllib
import matplotlib.pyplot as plt
import matplotlib.path as mplpath
import numpy as np
import cv2
from PIL import Image
import glob
import argparse
from imageCanvas import *
from stackPointConversion import *

sys.path.append('/home/gayathrim/libraries/render-python')

import renderapi

'''
render_connect = {
    'host': 'http://em-131fs',
    'port': 8080,
    'owner': 'gayathri',
    'project': 'EM_Phase1',
    'client_scripts': '/data/em-131fs/code/render/render-ws-java-client/src/main/scripts/',
    'memGB': '2G'}
'''

def convertFromScreenToWorld(screenCoords, secBounds, img_width):
    # converts the screen coordinates to world coordinates
    bounds_width = secBounds['maxX'] - secBounds['minX']
    bounds_height = secBounds['maxY'] - secBounds['minY']

    scale = img_width*1.0/bounds_width

    worldCoords = []
    for x, y in screenCoords:
        # convert the points to world coordinates
        x = (x/scale) + secBounds['minX']
        y = (y/scale) + secBounds['minY']
        worldCoords.append([x, y])

    return worldCoords



def extractAndLoadTilesFromSection(filenames, params, screenCoords, r):

    tsjsons = []
    for f in filenames:
        # assumes that the downsampled images are named after their z value
        pos = f.rfind('/')
        z = int(f[pos+1:-4])

        # do not write those sections that are not in the specified range
        if not (params["minZ"] <= z <= params["maxZ"]):
            continue

        # Get tile specs this is required to reupload sections with only selected tiles
        tilespecs = renderapi.tilespec.get_tile_specs_from_z(
            params["sourceStack"], z, render=r)

        # get section bounds
        secBounds = renderapi.stack.get_bounds_from_z(
            params["sourceStack"], z, render=r)

        # get section ID
        sectionId = tilespecs[0].layout.sectionId

        # PIL doesn't read the entire image... We just need the image dimensions
        #with Image.open(f) as img:
        #    img_width, img_height = img.size
        img = cv2.imread(f)
        img_width = img.shape[1]

        worldCoords = convertFromScreenToWorld(screenCoords, secBounds, img_width)

        try:
            tilespecs_inside = select_tilespecs_inside_polygon(
                worldCoords, tilespecs)
        except IndexError:
            print "no polygon defined for {}!".format(sectionId)
            tilespecs_inside = tilespecs

        # generate temporary json files
        tempjson = tempfile.NamedTemporaryFile(
            suffix='.json', mode='r', delete=False)
        tempjson.close()
        tsjson = tempjson.name
        with open(tsjson, 'w') as f:
            renderapi.utils.renderdump(tilespecs_inside, f)

        tsjsons.append(tsjson)

    return tsjsons



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select ROI by drawing a polygon')
    parser.add_argument('--jsonfile', '-j', dest='jsonfile', help='input json file with input parameters', type=str, default=None)
    args = parser.parse_args()

    if args.jsonfile is None:
        print "Need an input json file with input parameters"
        sys.exit()

    with open(args.jsonfile) as ipJson:
        params = json.load(ipJson)

    render_connect = {
        'host': params["baseUrl"],
        'port': 8080,
        'owner': params["owner"],
        'project': params["project"],
        'client_scripts': '/data/em-131fs/code/render/render-ws-java-client/src/main/scripts/',
        'memGB': '2G'
    }

    r = renderapi.connect(**render_connect)

    tsjsons = []

    # read the downscaled image of each section
    ext = "*." + params["ext"]
    files = glob.glob(os.path.join(params["downsampledImgPath"], ext))

    tsjsons = []
    screenCoords = []
    for i, f in enumerate(files):
        if (os.path.isfile(f)):
            #if ((i >= 0 and params["applyToAll"] == 0) or (i == 0 and params["applyToAll"] == 1)):
            # set up the image canvas to show the downscaled image and get the polygon roi
            canvasImage = imageCanvas(f)

            # show the image to get some polygons on it
            canvasImage.showImage()

            # get the screen coordinates of the polygon for the good section
            try:
                screenCoords = canvasImage.polygon[0].getScreenCoords()
            except IndexError:
                continue
            break

    tsjsons = extractAndLoadTilesFromSection(files, params, screenCoords, r)
    #tsjsons.append(tsjson)

    renderapi.stack.create_stack(params["targetStack"], render=r)
    # upload tilespecs -- TODO add pool setup
    renderapi.client.import_jsonfiles_parallel(
        params["targetStack"], tsjsons, poolsize=10, render=r)
    for tsjson in tsjsons:
        os.remove(tsjson)

'''

    inputStack = 'Phase1RawData_AIBS'
    targetStack = 'PolygonTest'

    r = renderapi.connect(**render_connect)


    downsampledImgPath = "/data/em-131fs/gayathri/downsampledSections"
    ext = "jpg"
    z = 2267

    # sp = stackPointConversion()
    tsjsons = []
    # Read the downscaled image of each section
    files = os.listdir(downsampledImgPath)
    for f in files:
        f = os.path.join(downsampledImgPath, f)
        if (os.path.isfile(f) and f.endswith(ext)):
            # assumes that the downsampled images are named after their z value
            z = int(f[len(downsampledImgPath)+1:-4])
            # sectionId = str(z) + '.0'
            # print sectionId

            # this is required to reupload sections with only selected tiles
            # tileSpecs = sp.getTileSpecs(stack, z)
            # print tileSpecs[0]
            tilespecs = renderapi.tilespec.get_tile_specs_from_z(
                inputStack, z, render=r)

            # get section bounds
            # secBounds = sp.getSectionBounds(stack, z)
            secbounds = renderapi.stack.get_bounds_from_z(
                inputStack, z, render=r)

            # get section ID
            # sectionId = tileSpecs[0]["layout"]["sectionId"]
            sectionId = tilespecs[0].layout.sectionId
            # print sectionId

            # get the bounds of all tiles in this section
            # tileBounds = sp.getTileBounds(stack, z)

            # set up the image canvas to show the downscaled image and get the polygon roi
            canvasImage = imageCanvas(f)

            # show the image to get some polygons on it
            canvasImage.showImage()

            # convert the polygon points to world coordinates using section bounds
            # canvasImage.convertPolygonPointsToWorld(secBounds)
            canvasImage.convertPolygonPointsToWorld(secbounds)

            # find the tiles whose center falls within this polygon
            # print canvasImage.polygon[0].worldCoords
            # tileIDs = sp.selectTilesInsidePolygon(
            #     canvasImage.polygon[0].worldCoords, tileBounds)
            # print tileIDs
            try:
                tilespecs_inside = select_tilespecs_inside_polygon(
                    canvasImage.polygon[0].worldCoords, tilespecs)
            except IndexError:
                print "no polygon defined for {}!".format(sectionId)
                tilespecs_inside = tilespecs

            # extract the tile specs corresponding to these tileIDs
            # tileSpecs = sp.getTileSpecsFromTileID(stack, tileIDs)
            # print tileSpecs

            # generate temporary json files
            tempjson = tempfile.NamedTemporaryFile(
                suffix='.json', mode='r', delete=False)
            tempjson.close()
            tsjson = tempjson.name
            with open(tsjson, 'w') as f:
                renderapi.utils.renderdump(tilespecs_inside, f)

            tsjsons.append(tsjson)

    renderapi.stack.create_stack(targetStack, render=r)
    # upload tilespecs -- TODO add pool setup
    renderapi.client.import_jsonfiles_parallel(
        targetStack, tsjsons, poolsize=10, render=r)
    for tsjson in tsjsons:
        os.remove(tsjson)
'''
