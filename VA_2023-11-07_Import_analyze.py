import pandas as pd

# Load the CSV file into a DataFrame
election_df = pd.read_csv('VA_Election Turnout_2023-11-07.csv')

# Display the first few rows of the DataFrame to verify the data has been imported correctly
print(election_df.head())
print(election_df.columns)
# ['election', 'election_date', 'locality', 'precinct', 'Early Voting', 'Provisional', 'Election Day', 'Mailed Absentee', 'Post-Election',
#  'TotalVoteTurnout', 'ActiveRegisteredVoters', 'InactiveRegisteredVoters', 'TotalRegisteredVoters', '% (totalTurnout_Active)']

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

merged_df = county_gdf.merge(election_df, how='left', left_on='PrecinctFullName', right_on='precinct')

# Plot the turnout by precinct
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
merged_df.plot(column='% (totalTurnout_Active)', ax=ax, legend=True, cmap='OrRd', edgecolor='black')
ax.set_title('Turnout by Precinct')
plt.show()

