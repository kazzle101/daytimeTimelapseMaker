# Daytime Video Timelapse

A Python script that saves an image from a USB camera during the hours of daylight, from dawn till dusk.

## Installation
Copy the files to a directory, the **imageFrames** and **videoCap** directories will be crerated when first run, the *tlphotos.json* file will be created with defults if it doesn't exist.

- tlphotos.py - captures the images
- tlcombine.py - combines the captured images to a video file.

You may need to add astral, OpenCV and argparse:
```
pip install astral
pip install opencv-python
pip install argparse
```

## Setup

Settings can be found in the **tlphotos.json** file, these are edititable, the others are automatically updated:
```
    "saveImages": true,
    "saveVideo": false,
    "videoFPS": 8,
    "dawnOffsetMinutes": -40,
    "duskOffsetMinutes": 40
```
the *saveImages* - true to save the jpg images, *saveVideo* - this is supposed to append the images to a video file, currently is does not work, *videoFPS* is related to saveVideo. *dawnOffsetMinutes* and *duskOffsetMinutes* - this starts the image taking before dawn and after dusk, currently 40 minutes either side.

For dawn and dusk to be calculated properly, set your location at the top of **tlphotos.py**
```
_lat, _lon = 53.47, -2.25
_city = LocationInfo("Manchester", "England", "Europe/London", _lat, _lon)
```

Use the cron to run the script, eg:
``` 
$ crontab -e
```
if asked, select nano as the editor then add:
```
*/5 * * * * python ~/Programming/daytimelapse/tlphotos.py
```
with '**~/Programming/daytimelapse/**' being the path to where you saved the script. This takes an image every five minutes.


## Combining the JPG files to a video

**tlcombine.py** is a utility for combining the jpgs to a video file
```
$ python tlcombine.py --help
usage: tlcombine.py [-h] [-d DIR] [-o OUT] [-r] [-f FPS]

combines JPG files into an AVI file

options:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  source directory
  -o OUT, --out OUT  output filename .avi
  -r, --recursive    recursivley walk through the directory
  -f FPS, --fps FPS  framerate
  -t, --timestamp    add a timestamp to the bottom right of the first 25 frames of the day
```
for example:
```
$ python tlcombine.py -r -d imageFrames/ -o videoCap/timeview.avi -f 8 -t
output file: videoCap/timeview.avi
458 images to combine at 8fps
```
the extention on the output file will always be set to .avi

Experiment with the FPS, this is the amount of time each frame is shown in the output video, for me this works best with a low number for when you only have a few days of images, but can be increased as you get more weeks of images.
  






