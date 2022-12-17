# Daytime Video Timelapse

A Python script that saves an image from a USB camera during the hours of daylight.

Use the cron to run the script, eg:
``` 
$ crontab -e
```
if asked, select nano as the editor then add:
```
*/5 * * * * python ~/Programming/daytimelapse/tlphotos.py
```
with '~/Programming/daytimelapse/' being the path to where you saved the script. This takes an image evry five minutes

Other settings can be found in the tlphotos.json file, these are edititable, the others are automatically updated:
```
    "saveImages": true,
    "saveVideo": false,
    "videoFPS": 8,
    "dawnOffsetMinutes": -40,
    "duskOffsetMinutes": 40
```
the saveImages - true to save the jpg images, saveVideo - this is supposed to append the images to a video file, currently is does not work, videoFPS is related to saveVideo.

dawnOffsetMinutes and duskOffsetMinutes - this starts the image taking before dawn and after dusk, currently 40 minutes either side.

tlcombine.py is a utility for combining the jpgs to a video file:



