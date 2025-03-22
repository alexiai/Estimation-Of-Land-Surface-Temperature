# 🌡️ Land Surface Temperature Downscaling Project

> 📌 **Author:** *Cojan Alexia Ilaria*  
> 🤝 *AI algorithm developed in collaboration with*: Roberto-Marian Chiper & Andrei-Mihai Diaconescu-Armasescu  

---

## ⚙️ Project Summary

This repository presents a web application designed and implemented **entirely by Cojan Alexia Ilaria**, focusing on estimating **Land Surface Temperature (LST)** using satellite data. The app integrates:

- A complete **frontend-backend architecture**, created from scratch in WebStorm
- A **Node.js backend** and **modern frontend** with full client-server interaction
- An **AI-based module** for LST estimation using satellite data

> 🔬 *The logic behind the AI model (LST estimation) was developed together with my colleagues, but the full application — from code organization to backend logic, server integration and frontend UI — was entirely implemented by me.*

---

## 🧠 AI Component: LST Downscaling using Google Earth Engine

### 📂 Scripts:

1. `gee.py`: Handles data collection, preprocessing, regression and downscaling in **Google Earth Engine**
2. `printer.py`: Visualizes and compares results using **Python (rasterio, matplotlib)**

---

### 🛰️ `gee.py` - Main Workflow

1. **Region & Date Selection**  
   Defines a polygon ROI (near Cluj-Napoca) and a date range

2. **Satellite Data Collection**  
   - Landsat 8 & Sentinel-2 imagery with <5% cloud cover
   - Data is scaled to reflectance and temperature

3. **Spectral Indices Calculated**  
   - NDVI 🌿 (Vegetation)
   - NDBI 🏙️ (Built-up)
   - NDWI 💧 (Water)

4. **Multiple Linear Regression**  
   Uses Landsat indices to model LST  
   ![Regression Equation](https://github.com/user-attachments/assets/0c064fe6-4105-4a76-bc02-891755ac9f00)

5. **Downscaling**  
   Applies the regression to Sentinel-2 for **10m resolution LST**

6. **Residual Correction**  
   Gaussian smoothing improves the accuracy of predictions

7. **Export**  
   All outputs saved as GeoTIFFs to Google Drive

---

### 📊 `printer.py` - Visualization Script

- **Reads and Plots GeoTIFFs**
- **Compares Landsat 8 vs Sentinel-2 results**
- **Displays metadata** (CRS, resolution, sample values)

---

## 🛠️ How to Run

### 🔧 Requirements
- Python 3.x
- Libraries: `rasterio`, `matplotlib`, `numpy`, `os`
- Google Earth Engine Python API

### 🚀 Execution Steps

1. Run `gee.py`  
   - Authenticate with GEE  
   - Exports LST + indices to Drive

2. Run `printer.py`  
   - Set the `folder_path` to exported data  
   - Use `plot_comparison()` for visual insights  
   - Use `printOne()` to display file metadata

---

---

## 🎥 Demo Video

[▶️ Click here to download and watch the video demo](https://drive.google.com/file/d/1sTktpgRfE6f2Y9g4Sxj3Fb2MxqkTwQLV/view?usp=sharing)

---

## 📤 Output

- ✅ 10m LST raster
- ✅ NDVI, NDBI, NDWI indices
- ✅ Comparison plots
- ✅ GeoTIFF metadata

---

## 📚 Bibliography

- [Google Earth Engine Documentation](https://developers.google.com/earth-engine)
- [Copernicus Open Access Hub](https://scihub.copernicus.eu/)
- [USGS EarthExplorer](https://earthexplorer.usgs.gov/)
- **Research Paper**:  
  *Onačillová et al. (2022), Remote Sensing, 14(16), 4076*  
  [DOI Link](https://doi.org/10.3390/rs14164076)

---

## 👥 Team

- **Cojan Alexia Ilaria** – *Full application development (frontend + backend)*  
- **Chiper Roberto-Marian** – *AI methodology contributor*  
- **Diaconescu-Armasescu Andrei-Mihai** – *AI methodology contributor*
