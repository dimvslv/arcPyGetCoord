This is a stub project created by the ArcGIS Desktop Python AddIn Wizard.

MANIFEST
========

README.txt   : This file

makeaddin.py : A script that will create a .esriaddin file out of this 
               project, suitable for sharing or deployment

config.xml   : The AddIn configuration file

Images/*     : all UI images for the project (icons, images for buttons, 
               etc)

Install/*    : The Python project used for the implementation of the
               AddIn. The specific python script to be used as the root
               module is specified in config.xml.

NOTES
========

## ✅ v1.0
- Creates a temporary layer with annotations as polylines.
- Records vertex coordinates in the attribute table and displays x, y labels.
- Works **only in coordinate systems that use meters (projected CRS).**
- Creates multiple temporary layers instead of overwriting.

## 🚀 How to Install
1. Clone the repository.
2. Run the file: `..\getCoordV1.0\getCoord.esriaddin`
3. Open or restart ArcMap.
4. A new button should appear in the toolbar.
5. Select objects, click the button, and get coordinates!
