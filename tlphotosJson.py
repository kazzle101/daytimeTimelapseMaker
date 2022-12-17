
import sys
from datetime import datetime, timezone, timedelta
from dateutil.tz import gettz # sudo pip install python-dateutil
import json
import os
import re

if __name__ == "__main__":
    print("this python script only works from: tlphotos.py")
    sys.exit(0)

class TLphotosJson:

    def __init__(self, settings):
        self.settings = settings

    def strToBool(self, d):

        if type(d) == bool:
            return d

        these = ["yes","1", "true", "ok"]
        d = str(d).lower().strip()
        if d in these:
            return True

        return False

    def strToDatetime(self, data):
        dtPattern = r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}) ([A-Z]{3})$'

        if type(data) != str:
            return data

        if not re.match(dtPattern, data):
            return data

        tzstr = data.rsplit(" ",1)[-1] or data
        tz = gettz(tzstr)
        if tz == None:
            tz = gettz("UTC")

        offset = tz.utcoffset(datetime.now()).total_seconds() / 3600

        dt = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S %Z")
        dt = dt.replace(tzinfo=timezone(timedelta(hours=offset)))
        return dt

    def loadSettingsFile(self):

        settingsFile = os.path.join(self.settings["scriptDir"], self.settings["settingsFile"])
        if not os.path.isfile(settingsFile):
            data = {}
            data["lastRun"] = self.settings["utcNow"]
            data["frameCount"] = 0
            err, msg = self.saveJSONfile(self.settings["scriptDir"], self.settings["settingsFile"], data)
            if err:
                print(f"error: {msg}")
                sys.exit(0)

            return data
        
        with open(settingsFile, 'r', encoding='utf-8') as f:
            try:    
                jsonData = json.load(f)
            except Exception as e:
                print(f"Error Loading JSON File: {settingsFile}")
                print(f"{e}")
                sys.exit(0)

        for key in jsonData:
            jsonData[key] = self.strToDatetime(jsonData[key])


        return jsonData


    def saveJSONfile(self, outputPath, outputFilename, data):
        
        pData = {}
        for key in data:
            if isinstance(data[key], datetime):
                pData[key] = data[key].strftime("%Y-%m-%dT%H:%M:%S %Z")
            else:
                pData[key] = data[key]

        if not "saveImages" in pData:
            pData["saveImages"] = True

        if not "saveVideo" in pData:
            pData["saveVideo"] = True

        if not "pyVersion" in pData:
            pData["pyVersion"] = sys.version

        if not "videoFPS" in pData:
            pData["videoFPS"] = 8

        if not "dawnOffsetMinutes" in pData:
            pData["dawnOffsetMinutes"] = -40

        if not "duskOffsetMinutes" in pData:
            pData["duskOffsetMinutes"] = 40

        filename = os.path.join(outputPath, outputFilename)
        # print(f"Saving json data to: {filename}")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(pData, f, ensure_ascii=False, indent=4)
        except IOError as e:                    
            return True, f"cannot write to: {filename}\nError: {e.errno}"

        return False, "ok"