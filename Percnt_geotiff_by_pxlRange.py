# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:35:02 2023

@author: Jalpesh
"""


import rasterio
import numpy as np
import pandas as pd

lower_threshold = 10
# upper_threshold = 100
# Example usage
index = 'TCI'
season = 'sum' # 'sum'
df1 = []


def percentage_cal(vhi_file_path, year, season):
        with rasterio.open(vhi_file_path) as src:
            # Read the VHI values
            vhi_values = src.read(1, masked=True)
        
            # Create a mask for non-NaN values
            valid_mask = ~np.isnan(vhi_values)
        
            # Count the number of non-NaN pixels with values between the specified thresholds
            count_between_thresholds = np.sum((vhi_values <= lower_threshold)  & valid_mask) #& (vhi_values <= upper_threshold)
        
            # Calculate the total number of non-NaN pixels
            total_valid_pixels = np.sum(valid_mask)
        
            # Calculate the percentage
            percentage_between_thresholds = (count_between_thresholds / total_valid_pixels) * 100
        
        print(f"Percentage of non-NaN pixels with values between {lower_threshold} : {percentage_between_thresholds:.2f}%") #and {upper_threshold}
        # Create a DataFrame
        data = {'Year': [year],
                'Season': [season],
                'Range': f'<{lower_threshold} ', #to {upper_threshold}
                'Percentage': [percentage_between_thresholds]}
        df = pd.DataFrame(data)
        df1.append(df)


for year in range(2001,2023):
    # Path to your VHI GeoTIFF file
    vhi_file_path = f'J:/VHI_Calc/{index}/{season}/Cropland/{index}_Cropland_{year}.tif'
    percentage_cal(vhi_file_path, year, season)
    
merged_df = pd.concat(df1, ignore_index=True)
# merged_df.to_excel(f'J:/VHI_Calc/{index}/{season}/Cropland/{index}_{season}.xlsx', sheet_name = f'<{lower_threshold}', index=True) #to{upper_threshold}

# Generate a sheet name based on the threshold values
sheet_name = f'<{lower_threshold}' #to{upper_threshold}

# Append the DataFrame to the Excel file with the dynamically generated sheet name
with pd.ExcelWriter(f'J:/VHI_Calc/{index}/{season}/Cropland/{index}_{season}.xlsx', engine='openpyxl', mode='a') as excel_writer:
    merged_df.to_excel(excel_writer, sheet_name=sheet_name, index=True)