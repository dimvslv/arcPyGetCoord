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

## ✅ v1.1
- Creates a temporary layer with points at the vertices of selected geometries.
- Records vertex coordinates in the attribute table and displays x, y labels.
- Supports all geometry types.
- Works in different coordinate systems.
- Fixed duplicated first and last points for "POLYGON" objects, as in v1.0.
- Creates multiple temporary layers instead of overwriting, as in v1.0.

## 🚀 How to Install
1. Clone the repository.
2. Run the file: `..\getCoordV1.1\getCoord.esriaddin`
3. Open or restart ArcMap.
4. A new button should appear in the toolbar.
5. Select objects, click the button, and get coordinates!
