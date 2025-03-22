import rasterio
import matplotlib.pyplot as plt
import os
import numpy as np

# Path to the folder containing the .tif files
folder_path = "image_ee"  # Update to your actual folder path

# Function to read a .tif file and return the data
def read_tif(file_path):
    with rasterio.open(file_path) as dataset:
        data = dataset.read(1)  # Read the first band
        return data

def plot_comparison(folder_path, indices):
    # Prepare the plot
    fig, axs = plt.subplots(len(indices), 2, figsize=(16, 16))
    
    # Ensure axs is always a 2D array for consistent indexing
    if len(indices) == 1:
        axs = np.array([axs])
    
    # Loop through each index
    for i, index in enumerate(indices):
        # Build file paths for Landsat 8 and Sentinel 2 for the current index
        l8_file = os.path.join(folder_path, f"l8_{index}.tif")
        s2_file = os.path.join(folder_path, f"s2_{index}.tif")
        
        # Check if both files exist and process them
        if os.path.exists(l8_file) and os.path.exists(s2_file):
            # Read both Landsat 8 and Sentinel 2 images for the current index
            l8_data = read_tif(l8_file)
            s2_data = read_tif(s2_file)
            
            # Calculate the min and max values for this index group
            vmin = min(np.nanmin(l8_data), np.nanmin(s2_data))
            vmax = max(np.nanmax(l8_data), np.nanmax(s2_data))
            
            # Plot the Landsat 8 image
            cmap = 'coolwarm'
            if (index == 'ndwi'):
                cmap = 'Blues'
            elif (index == 'ndbi'):
                cmap = 'OrRd'
            elif (index == 'ndvi'):
                cmap = 'RdYlGn'

            ax_l8 = axs[i, 0]
            cax_l8 = ax_l8.imshow(l8_data, cmap=cmap, vmin=vmin, vmax=vmax)
            ax_l8.set_title(f"Landsat 8 {index.upper()}")
            
            # Plot the Sentinel 2 image
            ax_s2 = axs[i, 1]
            cax_s2 = ax_s2.imshow(s2_data, cmap=cmap, vmin=vmin, vmax=vmax)
            fig.colorbar(cax_s2, ax=ax_s2, orientation='vertical')
            ax_s2.set_title(f"Sentinel 2 {index.upper()}")
    
    plt.tight_layout()
    plt.show()

# Example usage
plot_comparison("image_ee", ['ndwi', 'ndbi', 'ndvi'])
plot_comparison("image_ee", ['lst'])


def printOne(file_path):
    with rasterio.open(file_path) as dataset:
        # Read the image data as a numpy array
        data = dataset.read(1)  # Read the first band

        # Print basic information about the .tif file
        print(f"CRS (Coordinate Reference System): {dataset.crs}")
        print(f"Dimensions: {data.shape}")
        print(f"Data Type: {data.dtype}")
        print(f"Data values (first 10 values): {data.flatten()[:10]}")

        # Plot the image data
        plt.figure(figsize=(7, 9))
        plt.imshow(data, cmap='coolwarm')
        plt.colorbar(label='Pixel Value')
        plt.title(file_path)
        plt.show()

# printOne("image_ee/first_downscale.tif")
# printOne("download.constant.tif")