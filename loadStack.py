
# Takes a render stack and a z-value for a section and reads in all the parameters required for locating tiles location in the downsampled images

import os, sys, json
import urllib


def loadTileSpecs(stack,z):
    # stack - a structure that contains the baseUrl, owner, project, stackname, etc.
    # z - z-value of the section

    # get a list of all tiles
    urlChar = stack["baseUrl"] + '/owner/' + stack["owner"] + '/project/' + stack["project"] + '/stack/' + stack["stackname"] + '/z/' + str(z) + '.0' + '/tile-specs'
    f = urllib.urlopen(urlChar)
    data = json.loads(f.read())
    return data

def loadTileData(stackJsonData):
    tileData = []
    for jt in stackJsonData:
        

if __name__ == '__main__':
    stack = {}
    stack["baseUrl"] = "http://em-131fs:8080/render-ws/v1"
    stack["owner"] = "gayathri"
    stack["project"] = "EM_Phase1"
    stack["stackname"] = "Phase1RawData_AIBS"
    z = 2267

    tileSpecs = loadTileSpecs(stack,z)

    # get section ID
    sectionId = tileSpecs[0]["layout"]["sectionId"]
    print sectionId
