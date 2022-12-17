#!/usr/bin/env python

import argparse
import os
import cv2
import sys
import fnmatch

_scriptDir = os.path.dirname(os.path.realpath(__file__))

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

def main():

    desc = """combines JPG files into an AVI file"""

    epilog = """"""

    parser = argparse.ArgumentParser(description=desc, epilog=epilog)
    parser.add_argument("-d", "--dir", type=str, help="source directory")
    parser.add_argument("-o", "--out", type=str, help="output filename .avi")
    parser.add_argument("-r", "--recursive", action='store_true', help="recursivley walk through the directory")
    parser.add_argument("-f", "--fps", type=int, default=10,  help="framerate")

    args = parser.parse_args()

    if not args.dir:
        print("source directory not given")
        sys.exit(0)

    if not args.out:
        print("output file not given")
        sys.exit(0)

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
    aviFile = cv2.VideoWriter(outputFile, fourcc, framerate, (1920, 1080))

    for img in imgList:
        image = cv2.imread(img)
        aviFile.write(image)

    aviFile.release()

    return

if __name__ == "__main__":
    main()