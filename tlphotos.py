#!/usr/bin/env python

from datetime import datetime, timezone, timedelta
from astral import LocationInfo
from astral.sun import sun
import argparse
import os
import cv2
import sys

from tlphotosJson import TLphotosJson

_lat, _lon = 53.39, -1.48
_city = LocationInfo("Sheffield", "England", "Europe/London", _lat, _lon)
_scriptDir = os.path.dirname(os.path.realpath(__file__))
_settingsFile = "tlphotos.json"
_utcNow = datetime.now(timezone.utc)

def main():
    os.chdir(_scriptDir)
    settings = { 
        "scriptDir" : _scriptDir,
        "settingsFile" : _settingsFile,
        "utcNow" : _utcNow
    }
    photosJson = TLphotosJson(settings)

    settingsJSON = photosJson.loadSettingsFile()

    settingsChanged = False

    # desc = """Makes a timelapse while the sun is up"""

    # epilog = """Creates a timelapse from an attached usb video device between dawn and dusk
    #             run from a cronjob"""

    # parser = argparse.ArgumentParser(description=desc, epilog=epilog)
    # parser.add_argument("-s", "--saveimages", type=str, help="set to true to save images (default)")
    # parser.add_argument("-v", "--savevideo", type=str, help="set to true to save video (default)")

    imageDir = os.path.join(_scriptDir,"imageFrames")
    if not os.path.isdir(imageDir):
        os.mkdir(imageDir)

    videoDir = os.path.join(_scriptDir, "videoCap")
    if not os.path.isdir(videoDir):
        os.mkdir(videoDir)


    s = sun(_city.observer, date=_utcNow, tzinfo=timezone.utc)
    settingsJSON["lastRun"] = _utcNow # .strftime("%Y-%m-%dT%H:%M:%S %Z")
    settingsJSON["sunrise"] = s["sunrise"].strftime("%Y-%m-%dT%H:%M:%S %Z")
    settingsJSON["sunset"] = s["sunset"].strftime("%Y-%m-%dT%H:%M:%S %Z")
    settingsJSON["dawn"] = s["dawn"].strftime("%Y-%m-%dT%H:%M:%S %Z")
    settingsJSON["dusk"] = s["dusk"].strftime("%Y-%m-%dT%H:%M:%S %Z")

    # print((
    #     f'Dawn:    {s["dawn"]}\n'
    #     f'Sunrise: {s["sunrise"]}\n'
    #     f'Noon:    {s["noon"]}\n'
    #     f'Sunset:  {s["sunset"]}\n'
    #     f'Dusk:    {s["dusk"]}\n'
    # ))

    dawnOffset = abs(settingsJSON["dawnOffsetMinutes"])
    duskOffset = abs(settingsJSON["duskOffsetMinutes"])

    settingsJSON["dawnMinus"] = s["dawn"] - timedelta(minutes=dawnOffset)
    settingsJSON["duskPlus"] = s["dusk"] + timedelta(minutes=duskOffset)

    if _utcNow < settingsJSON["dawnMinus"]:
        settingsJSON["status"] = "before dawn"
        photosJson.saveJSONfile(_scriptDir, _settingsFile, settingsJSON)
        return

    if _utcNow > settingsJSON["duskPlus"]:
        settingsJSON["status"] = "after dusk"
        photosJson.saveJSONfile(_scriptDir, _settingsFile, settingsJSON)
        return

    # print(settingsJSON)

    imageDir = os.path.join(imageDir,_utcNow.strftime("%Y%m%d"))
    if not os.path.isdir(imageDir):
        os.mkdir(imageDir)

    imageFile = "{}_tl.jpg".format(_utcNow.strftime("%Y%m%d_%H%M%S"))
    imageFile = os.path.join(imageDir, imageFile)

    videoFile = "{}_tl.avi".format(_utcNow.strftime("%Y%m%d"))
    videoFile = os.path.join(videoDir, videoFile)

    cap = cv2.VideoCapture(0)  # use 0 to capture from the default camera

    if settingsJSON["saveVideo"]: 
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        aviFile = cv2.VideoWriter(videoFile, fourcc, settingsJSON["videoFPS"], (1920, 1080))
        
    f=0
    status = "ok"
    timeout = _utcNow + timedelta(seconds=5)
    while True:
        now = datetime.now(timezone.utc)

        ret, frame = cap.read()
        if ret:
            if settingsJSON["saveImages"]:
                cv2.imwrite(imageFile, frame)

            if settingsJSON["saveVideo"]:      
                aviFile.write(frame)

            f +=1

        if f >= 1:
            break

        if now > timeout:
            print("timeout")
            status = "timeout"
            break

    cap.release()

    if settingsJSON["saveVideo"]: 
        aviFile.release()

    settingsJSON["frameCount"] += 1
    settingsJSON["status"] = status
    photosJson.saveJSONfile(_scriptDir, _settingsFile, settingsJSON)
    return

if __name__ == "__main__":
    main()
