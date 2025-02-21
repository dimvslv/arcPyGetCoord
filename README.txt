# 🗺 arcPyGetCoord - ArcGIS Add-in

## 📍 Project Description
arcPyGetCoord is an ArcGIS add-in that allows ArcMap users to extract vertex coordinates 
from selected geometries and display them in attribute tables and annotations. 
Different versions offer unique functionalities and improvements.

## 📂 Structure
arcPyGetCoord/ 
├── v1.0/ # Initial version 
├── v1.1/ # Improved polygon handling, multiple temporary layers 
├── v1.2/ # **Annotation** support, works **only** in projected CRS with meters 
├── README.md # Project description 
├── .gitignore # Ignored files

## 🔄 Versions

### ✅ v1.0
- Creates a temporary layer with points at the vertices of selected geometries.
- Records vertex coordinates in the attribute table and displays x, y labels.
- Supports all geometry types.
- Works in different coordinate systems.
- Overwrites the temporary layer on each iteration.

### ✅ v1.1
- Same functionality as v1.0.
- Fixed duplicated first and last points for "POLYGON" objects.
- Creates multiple temporary layers instead of overwriting.

### ✅ v1.2
- Creates a temporary layer with annotations as polylines.
- Records vertex coordinates in the attribute table and displays x, y labels.
- Works **only in coordinate systems that use meters (projected CRS).**
- Creates multiple temporary layers instead of overwriting.

## 🔧 Technologies Used
- **ArcGIS** – primary platform.
- **Python** – scripting and automation.
- **ArcPy** – ArcGIS Python API for geoprocessing.

## 🚀 How to Use
1. Choose the desired version from the repository.
2. Follow the installation and usage instructions inside the version's `README.md` file.

## 📜 License
This project is intended for educational and research use only.  
Commercial use, redistribution, or modification without permission is not allowed. Please contact me for details.

## 📧 Contact
Email: wasilev1994@gmail.com | GitHub: dimvslv
