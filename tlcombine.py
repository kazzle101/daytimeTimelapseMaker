#!/usr/bin/env python

import argparse
import os
import cv2
import sys
import fnmatch
import numpy as np
from datetime import datetime

_scriptDir = os.path.dirname(os.path.realpath(__file__))
_videoSize = { 'width': 1920, 'height': 1080}
_titleFrameMax = 25  ## adds a datetime stamp to the first XX frames on the bottom right of the day

def getRecursiveFilesList(dir):

    jpegFiles = []
    for root, dirs, files in os.walk(dir):
        jpegFilesInDir = fnmatch.filter(files, '*.jpg')

        jFiles = []
        for j in jpegFilesInDir:
            jFiles.append(os.path.join(root,j))

        jpegFiles.extend(jFiles)

    jpegFiles.sort(key=lambda x: os.stat(x).st_ctime)
    return jpegFiles

def getFilesList(dir):
    fileList = os.listdir(dir)
    fileList.sort(key=lambda x: os.stat(os.path.join(dir, x)).st_ctime)
    jpegFiles = fnmatch.filter(fileList, '*.jpg')
    
    jpgList = []
    for j in jpegFiles:
        jpgList.append(os.path.join(dir, j))

    return jpgList

def setOutputFilename(fn):
    name, ext = os.path.splitext(fn)
    return name + ".avi"

def addVideoText(image, text):

    height, width = image.shape[:2]    
    (tw,th), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 1, 1)

    x = width - tw - 8
    y = height - th - 8

    rectX = x - 5
    rectY = y + th
    rectWidth = tw + 10
    rectHeight = th - 30 # + 10

    cv2.rectangle(image, (rectX, rectY - 50), (rectX + rectWidth, rectY + rectHeight), (0, 0, 0), -1)
    cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
    return image

def getCreationDatetime(file):

    ctime = os.path.getctime(file)
    dt = datetime.fromtimestamp(ctime)

    dts = dt.strftime("%d %B %Y, %H:%M")
    return dts

def main():

    addTimestamp = False

    desc = """combines JPG files into an AVI file"""

    epilog = """"""

    parser = argparse.ArgumentParser(description=desc, epilog=epilog)
    parser.add_argument("-d", "--dir", type=str, help="source directory")
    parser.add_argument("-o", "--out", type=str, help="output filename .avi")
    parser.add_argument("-r", "--recursive", action='store_true', help="recursivley walk through the directory")
    parser.add_argument("-f", "--fps", type=int, default=10,  help="framerate")
    parser.add_argument("-t", "--timestamp", action='store_true', help=f"add a timestamp to the bottom right of the first {_titleFrameMax} frames of the day")

    args = parser.parse_args()

    if not args.dir:
        print("source directory not given")
        sys.exit(0)

    if not args.out:
        print("output file not given")
        sys.exit(0)

    if args.timestamp:
        addTimestamp = True

    framerate = args.fps

    if args.recursive:
        imgList = getRecursiveFilesList(args.dir)
    else:
        imgList = getFilesList(args.dir)

    if not imgList:
        print(f"no jpg images found in: {args.dir}")
        sys.exit(0)

    outputFile = setOutputFilename(args.out)

    print(f"output file: {outputFile}")
    print(f"{len(imgList)} images to combine at {framerate}fps")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    width, height = _videoSize["width"], _videoSize["height"]
    aviFile = cv2.VideoWriter(outputFile, fourcc, framerate, (width, height))

    titleFrameCount = 0
    dirList = []
    for img in imgList:
        image = cv2.imread(img)

        if addTimestamp:
            imgDir = os.path.dirname(img)
            if not imgDir in dirList:
                dirList.append(imgDir)
                titleFrameCount = 0

            if titleFrameCount < _titleFrameMax:
                text = getCreationDatetime(img)
                image = addVideoText(image, text)

            titleFrameCount += 1    

        aviFile.write(image)

    aviFile.release()

    return

if __name__ == "__main__":
    main()