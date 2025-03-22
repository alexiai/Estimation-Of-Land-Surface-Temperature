import ee
from datetime import datetime, timedelta


ee.Authenticate()
ee.Initialize(project="vibrant-keyword-447315-i0")

roi = ee.Geometry.Polygon([
    [
        [23.546, 46.804], [23.546, 46.732], [23.689, 46.732], [23.689, 46.804]
    ]
], None, False)

# Set initial date range
start_date = '2018-08-21'
end_date = '2018-08-28'
cloud_percentage = 5

# Convert date strings to datetime objects
start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

# Find a Landsat image by extending the end date until an image is found
l8 = None
max_days = 30  # Maximum number of days to extend the end date
days_extended = 0

while l8 is None or l8.getInfo() is None:
    if days_extended > max_days:
        raise Exception("No Landsat images found within 30 days of the initial date range.")

    l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
        .filterBounds(roi) \
        .filterDate(start_date, end_date_dt.strftime('%Y-%m-%d')) \
        .filterMetadata("CLOUD_COVER", "less_than", ee.Number(cloud_percentage)) \
        .first()

    if l8.getInfo() is None:  # Check if no image is found
        days_extended += 1
        end_date_dt += timedelta(days=1)

print(f"Landsat image found with end date: {end_date_dt.strftime('%Y-%m-%d')}")
print(l8.getInfo())

# Get Sentinel-2 collection
s2 = ee.ImageCollection('COPERNICUS/S2_SR') \
    .filterBounds(roi) \
    .filterDate(start_date, end_date_dt.strftime('%Y-%m-%d')) \
    .filterMetadata("CLOUDY_PIXEL_PERCENTAGE", "less_than", ee.Number(cloud_percentage)) \
    .median()


def applyScaleFactors(image):
    opticalBands = image.select('SR_B.*').multiply(0.0000275).add(-0.2).multiply(10000)
    thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0).subtract(273.15)
    return image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)


# Apply the scaling function to the Landsat selected dataset
l8 = applyScaleFactors(l8)

l8_ndvi = l8.normalizedDifference(['SR_B5', 'SR_B4']).rename('L8_NDVI')
l8_ndwi = l8.normalizedDifference(['SR_B3', 'SR_B5']).rename('L8_NDWI')
l8_ndbi = l8.normalizedDifference(['SR_B6', 'SR_B5']).rename('L8_NDBI')
l8_lst_30m = l8.select('ST_B10')

s2_ndvi = s2.normalizedDifference(['B8', 'B4']).rename('S2_NDVI')
s2_ndwi = s2.normalizedDifference(['B3', 'B11']).rename('S2_NDWI')
s2_ndbi = s2.normalizedDifference(['B11', 'B8']).rename('S2_NDBI')

bands = ee.Image(1).addBands(l8_ndvi).addBands(l8_ndbi)\
    .addBands(l8_ndwi).addBands(l8_lst_30m).rename(
    ["constant", "ndvi", "ndbi", "ndwi", "L8"])

# Run the multiple regression analysis
imageRegression = bands.reduceRegion(
    reducer=ee.Reducer.linearRegression(numX=4, numY=1),
    geometry=roi,
    scale=30
)

# Extract coefficients
coefList2 = ee.Array(imageRegression.get("coefficients")).toList()
a0 = ee.Image(ee.Number(ee.List(coefList2.get(0)).get(0)))
a1 = ee.Image(ee.Number(ee.List(coefList2.get(1)).get(0)))
a2 = ee.Image(ee.Number(ee.List(coefList2.get(2)).get(0)))
a3 = ee.Image(ee.Number(ee.List(coefList2.get(3)).get(0)))

downscaled_LST_10m = a0.add(a1.multiply(s2_ndvi)) \
    .add(a2.multiply(s2_ndbi)) \
    .add(a3.multiply(s2_ndwi))

# Calculate L8-LST 30 m model
L8_LST_MODEL = a0.add(a1.multiply(l8_ndvi)) \
    .add(a2.multiply(l8_ndbi)) \
    .add(a3.multiply(l8_ndwi)).clip(roi)

# Calculate residuals (difference between observed and model)
L8_RESIDUALS = l8_lst_30m.subtract(L8_LST_MODEL)

gaussian = ee.Kernel.gaussian(
    radius=1.5, units='pixels'
)

L8_RESIDUALS_gaussian = L8_RESIDUALS.resample("bicubic").convolve(gaussian)

S2_LST_10_w_Residuals = downscaled_LST_10m.add(L8_RESIDUALS_gaussian)


def exportToDrive(image, name):
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=name,
        folder="image_ee",
        scale=30,
        region=roi,
        fileFormat='GeoTIFF',
    )
    task.start()


def get_download_image_url(image, region):
    url = image.getDownloadURL({
        'scale': 30,
        'region': region,
        'fileFormat': 'GeoTIFF'
    })
    return url


# get_download_image_url(S2_LST_10_w_Residuals, roi)

exportToDrive(S2_LST_10_w_Residuals, "s2_lst")
exportToDrive(l8_lst_30m, "l8_lst")
exportToDrive(l8_ndvi, "l8_ndvi")
exportToDrive(l8_ndwi, "l8_ndwi")
exportToDrive(l8_ndbi, "l8_ndbi")
exportToDrive(s2_ndvi, "s2_ndvi")
exportToDrive(s2_ndwi, "s2_ndwi")
exportToDrive(s2_ndbi, "s2_ndbi")





