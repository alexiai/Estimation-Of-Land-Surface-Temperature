# Land Surface Temperature Downscaling Project

This project focuses on downscaling Land Surface Temperature (LST) from Landsat 8 satellite data to a higher resolution using Sentinel-2 data. The downscaling is performed by applying multiple linear regression and residual correction techniques. The project consists of two main components:
-	1.	gee.py: This script performs data collection, preprocessing, regression analysis, and downscaling using Google Earth Engine.
-	2.	printer.py: This script visualizes and compares the downscaled LST results using Python libraries such as rasterio and matplotlib.

 ## 1. gee.py: Downscaling LST using Google Earth Engine

Functionality
-	1.	Region of Interest (ROI) and Date Selection
The script defines a polygon representing the region of interest (ROI) and specifies a date range for image collection. The region selected is an urban area near Cluj-Napoca.
-	2.	Image Collection and Cloud Filtering
	-	Landsat 8 images are retrieved using the specified ROI and date range.
	-	Sentinel-2 images are also collected, and both datasets are filtered to ensure less than 5% cloud cover.
-	3.	Applying Scale Factors
Landsat 8 data are scaled to convert raw digital numbers into reflectance and temperature values.
-	4.	Spectral Index Calculation
The script calculates three key spectral indices for both Landsat 8 and Sentinel-2:
	-	NDVI (Normalized Difference Vegetation Index)
	-	NDBI (Normalized Difference Built-up Index)
	-	NDWI (Normalized Difference Water Index)
-	5.	Multiple Linear Regression
A multiple linear regression model is applied using Landsat 8 data, with the spectral indices as predictors and LST as the target variable:


<img width="254" alt="image" src="https://github.com/user-attachments/assets/0c064fe6-4105-4a76-bc02-891755ac9f00" />


The coefficients a_0, a_1, a_2, a_3 are extracted from the regression model.
-	6.	Downscaling LST
The regression model is applied to the higher-resolution Sentinel-2 indices to generate LST at 10m resolution.
-	7.	Residual Correction
Residuals between the observed and predicted LST are calculated, smoothed using a Gaussian kernel, and added to the downscaled LST to improve accuracy.
-	8.	Exporting Results
The downscaled LST and other calculated indices are exported as GeoTIFF files to Google Drive.

## 2. printer.py: Visualizing and Comparing Results

### Functionality
- Reading and Plotting GeoTIFF Files
The script reads the exported GeoTIFF files (LST and spectral indices) using rasterio and visualizes them using matplotlib.
- Comparing Landsat 8 and Sentinel-2 Results
- The function plot_comparison compares the indices and LST results from Landsat 8 and Sentinel-2 by plotting them side by side.
- Displaying File Information
The function printOne displays key metadata of a selected GeoTIFF file, such as:
	- 	Coordinate Reference System (CRS)
	- 	Dimensions
	- 	Data type
	- 	Sample data values

# How to Run the Project

- Requirements
- Python 3.x
- Installed Python libraries:
	-	rasterio
	-	matplotlib
	-	numpy
	-	os
- Google Earth Engine Python API

Steps to Execute
-	Run gee.py
	-	Ensure you are authenticated with Google Earth Engine.
	-	The script will download and process the required Landsat 8 and Sentinel-2 images.
	-	Downscaled LST and spectral indices will be exported to Google Drive as GeoTIFF files.
-		Run printer.py
  	- Update the folder_path variable with the path to the exported GeoTIFF files.
	-	Use plot_comparison to visualize the comparison between Landsat 8 and Sentinel-2 indices and LST.
	-	Use printOne to display metadata and visualize individual GeoTIFF files.

# Output

The project produces the following outputs:
-	1.	Downscaled LST at 10m resolution
-	2.	Spectral indices (NDVI, NDBI, NDWI) for Landsat 8 and Sentinel-2
-	3.	Plots comparing Landsat 8 and Sentinel-2 results
-	4.	Metadata of the exported GeoTIFF files

# Bibliography

The following resources were essential in the development of this project:
-	1.	Google Earth Engine API (ee)
Google Earth Engine provided a cloud-based platform for satellite data retrieval and processing.
Link: Google Earth Engine Documentation
-	2.	Python Programming Language
Python was used for implementing data visualization and export functionalities.
-	3.	Copernicus Open Access Hub
Sentinel-2 data were obtained through the Copernicus Open Access Hub.
Link: Copernicus Open Access Hub
-	4.	Landsat Data from USGS EarthExplorer
Landsat 8 data were downloaded using the USGS EarthExplorer platform.
Link: USGS EarthExplorer
-	5.	Research Article
The methodology for downscaling LST was inspired by the following research article:
Onačillová, K., Gallay, M., Paluba, D., Péliová, A., Tokarčík, O., & Laubertová, D. (2022). Combining Landsat 8 and Sentinel-2 Data in Google Earth Engine to Derive Higher Resolution Land Surface Temperature Maps in Urban Environment. Remote Sensing, 14(16), 4076.
Link: Research Article DOI

## Our Team:
Chiper Roberto-Marian
Cojan Alexia Ilaria
Diaconescu-Armasescu Andrei-Mihai

