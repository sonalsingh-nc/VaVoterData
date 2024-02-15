import pandas as pd


##  Download the ShapeZip Files
## https://www.elections.virginia.gov/casting-a-ballot/redistricting/gis/
import os
import requests
from bs4 import BeautifulSoup

# URL of the directory containing the ZIP files
url = 'https://www.elections.virginia.gov/casting-a-ballot/redistricting/gis/'
url2 = "https://www.elections.virginia.gov/media/redistricting/gis/-zip-files"

# Destination directory to save the downloaded ZIP files
destination_directory = 'D:\Sonal\Downloads\shapezip'

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all 'a' tags (links) in the HTML content
    links = soup.find_all('a')
    
    # Iterate through each link
    for link in links:
        # Get the href attribute of the link
        href = link.get('href')
        
        # Check if the href ends with .zip
        if href.endswith('.zip'):
            # Construct the full URL of the ZIP file
            filename = os.path.basename(href)
            zip_url = url2 + '/' + filename
            print(filename)
            print(zip_url)
            # https://www.elections.virginia.gov/                                   media/redistricting/gis/-zip-files/Bland_County.zip
            # https://www.elections.virginia.gov/casting-a-ballot/redistricting/gis/media/redistricting/gis/-zip-files/Williamsburg_City.zip

            # Extract the filename from the URL
            filename = os.path.basename(zip_url)
            
            # Download the ZIP file
            with open(os.path.join(destination_directory, filename), 'wb') as f:
                f.write(requests.get(zip_url).content)
                
            print(f"Downloaded {filename} successfully.")
else:
    print("Failed to retrieve the list of ZIP files.")

## Extract 
import os
import zipfile
import shutil

# Source directory containing the zip files
source_directory = 'D:\Sonal\Downloads\shapezip'

# Destination directory to extract .shp files
destination_directory = 'D:\Sonal\Documents\GitHub\VaVoterData\ShapeFiles'

# Iterate through each zip file in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith('.zip'):
        # Open the zip file
        with zipfile.ZipFile(os.path.join(source_directory, filename), 'r') as zip_ref:
            # Iterate through each file in the zip file
            for file_info in zip_ref.infolist():
                # Check if the file is a .shp file
                #if file_info.filename.endswith('.shp'):
                # Extract the .shp file to the destination directory
                zip_ref.extract(file_info, destination_directory)

# List the extracted .shp files
extracted_files = os.listdir(destination_directory)
print("Extracted .shp files:")
for file_name in extracted_files:
    print(os.path.join(destination_directory, file_name))



###
# Import Shape Files starting with Accomack County
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

destination_directory = 'D:\Sonal\Documents\GitHub\VaVoterData\ShapeFiles'
# Iterate through each shp file in the shapeFile directory
gdfs = []
for filename in os.listdir(destination_directory):
    if filename.endswith('.shp'):
        # Load the Shapefile for county boundaries with precincts
        print('filename is: '+filename)
        this_county_gdf = gpd.read_file(destination_directory+'\\'+filename)

        gdfs.append(this_county_gdf)

# Concatenate all GeoDataFrames into a single GeoDataFrame
county_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

# Print information about the merged GeoDataFrame
print("Merged GeoDataFrame:")
print(county_gdf.info())

# Display the first few rows of the DataFrame to verify the data has been imported correctly
print(county_gdf.head())
print(county_gdf.columns)
# 'CountyName', 'CountyFIPS', 'DistName', 'DistNumber', 'PrcnctNum', 'PrcnctFIPS', 'PrcnctName', 'PrcNmeLong', 'GEOID', 'LctnName','Shape_Leng', 'Shape_Area', 'geometry']
# Print selected columns
selected_columns = ['CountyName', 'CountyFIPS', 'PrcnctNum', 'PrcnctNum', 'PrcnctFIPS', 'PrcnctName']  # Specify the column names you want to print
print(county_gdf[selected_columns])


# Merge election data with county Shapefile data
# election_df: location = ACCOMACK COUNTY   precinct =  101 - CHINCOTEAGUE
# county_gdf: CountyName = Accomack County 
#      CountyName CountyFIPS PrcnctNum PrcnctNum PrcnctFIPS      PrcnctName
# 0   Accomack County        001        01        01     000701          Nandua
# 1   Accomack County        001        01        01     000601         Accomac
# 2   Accomack County        001        01        01     000201        Atlantic
# 3   Accomack County        001        01        01     000401          Bloxom
# 4   Accomack County        001        01        01     000801         Bobtown
# 5   Accomack County        001        01        01     000101    Chincoteague


# Define a function to create the PrecinctFullName
def create_full_name(row):
    return row['PrcnctFIPS'][-3:] + ' - ' + row['PrcnctName'].upper()

# Apply the function to create the new column
county_gdf['PrecinctFullName'] = county_gdf.apply(create_full_name, axis=1)

# Print the updated dataframe
print(county_gdf)

import geopandas as gpd

county_gdf.to_parquet('county_gdf.parquet')
# Part A: End of part, which creates downloads, Unzips and creates the Precinct Level ShapeFiles DataFrame
##################################################################################################




# Part B: Import Election Data, Merge it with the ShapeFile GDF
################################################################

import geopandas as gpd
import pandas as pd

# Read the DataFrame from the Parquet file
county_gdf = gpd.read_parquet('county_gdf.parquet')


# Load the CSV file into a DataFrame
election_df = pd.read_csv('VA_Election Turnout_2023-11-07.csv')

# Define a function to calculate the turnout percentage

def calculate_turnout_pct(row):
    if not pd.isna(row['ActiveRegisteredVoters']) and row['ActiveRegisteredVoters'] > 0:
        if not pd.isna(row['TotalVoteTurnout']):
            return row['TotalVoteTurnout'] / row['ActiveRegisteredVoters'] * 100
    return 0

# Apply the function to create the new column
election_df['Turnout_pct'] = election_df.apply(calculate_turnout_pct, axis=1)

# Display the first few rows of the DataFrame to verify the data has been imported correctly
print(election_df.head())
print(election_df.columns)
# ['election', 'election_date', 'locality', 'precinct', 'Early Voting', 'Provisional', 'Election Day', 'Mailed Absentee', 'Post-Election',
#  'TotalVoteTurnout', 'ActiveRegisteredVoters', 'InactiveRegisteredVoters', 'TotalRegisteredVoters', '% (totalTurnout_Active)']
merged_df = county_gdf.merge(election_df, how='left', left_on='PrecinctFullName', right_on='precinct')

# Add Precinct labels to the map  
# https://geopandas.org/en/stable/gallery/plotting_basemap_background.html
# Add a base map of Virginia as a layer

# Load the base map of Virginia
# <Geographic 2D CRS: EPSG:4326>
# Name: WGS 84
# Load the Virginia city and county census boundaries dataset
import geopandas as gpd
import matplotlib.pyplot as plt

virginia_boundaries = gpd.read_file('D:\Sonal\Documents\GitHub\VaVoterData\ShapeFiles\City_County\SDE_USDC_CENSUS_VA_COUNTY.shp')
virginia_boundaries.info()
print(virginia_boundaries)
print(virginia_boundaries[['NAME', 'NAMELSAD', 'LSAD','CLASSFP', 'COUNTYFP', 'COUNTYNS']])

# Filter out the cities (excluding counties)
virginia_cities = virginia_boundaries[virginia_boundaries['NAMELSAD'].str.contains('city')]
virginia_cities.info()
print(virginia_cities[['NAME', 'NAMELSAD', 'LSAD','CLASSFP', 'COUNTYFP', 'COUNTYNS']])

# Reproject the geometries to a projected CRS
virginia_cities = virginia_cities.to_crs('EPSG:3857')  # Example of a commonly used projected CRS (Web Mercator)
virginia_boundaries = virginia_boundaries.to_crs('EPSG:3857') 

# Plot the base map
ax = virginia_boundaries.plot(color='lightgrey', edgecolor='black' , linewidth=0.25)

# Plot the cities on top of the base map
virginia_cities.plot(ax=ax, color='lightblue', edgecolor='black', linewidth=0.50)

# Add city names as annotations
for x, y, label in zip(virginia_cities.geometry.centroid.x, virginia_cities.geometry.centroid.y, virginia_cities['NAME']):
    ax.text(x, y, label, fontsize=6, ha='center', va='top', color='black') 


# Plot the base map
# Plot the turnout by precinct on top of the base map
# First change the CRS (Co-ordinate Reference System) of the merged_df to match the base_map
merged_df = merged_df.to_crs('EPSG:3857')
merged_df.plot(column='Turnout_pct', ax=ax, legend=True, cmap='OrRd', edgecolor='grey', linewidth=0.20)

print(merged_df)

# Filter in the precincts with Voters > 4000  
merged_df_cities = merged_df[merged_df['ActiveRegisteredVoters'].gt(4000)]
merged_df_cities.info()


# Add callouts for each geometry in the GeoDataFrame
for idx, row in merged_df_cities.iterrows():
    Turnout_pct =  int(row['Turnout_pct']) if not pd.isna(row['Turnout_pct']) else 0
    ax.annotate(text=str(Turnout_pct), xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                xytext=(7, 7), textcoords="offset points", fontsize=6, ha='center', va='center', color='black')

ax.set_title('VA 2023-11-07 State Senate & House - Turnout by Precinct')
ax.axis('off')

# Show the plot
plt.show()

# Save the Plot as a PNG file in the same directory 
plt.savefig('VA 2023-11-07 State Senate & House - Turnout by Precinct.png')
