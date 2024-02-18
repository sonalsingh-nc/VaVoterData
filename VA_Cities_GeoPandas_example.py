import geopandas as gpd
import matplotlib.pyplot as plt

# Load the Virginia city and county census boundaries dataset
virginia_boundaries = gpd.read_file('D:\Sonal\Documents\GitHub\VaVoterData\ShapeFiles\City_County\SDE_USDC_CENSUS_VA_COUNTY.shp')
virginia_boundaries.info()
print(virginia_boundaries)

# Filter out the cities (excluding counties)
virginia_cities = virginia_boundaries[virginia_boundaries['NAMELSAD'].str.contains('city')]
virginia_cities.info()

# Plot the base map
ax = virginia_boundaries.plot(color='lightgrey', edgecolor='grey', linewidth=0.25)

# Plot the cities on top of the base map
virginia_cities.plot(ax=ax, color='lightblue', edgecolor='black' , linewidth=0.50)

# Add city names as annotations
for x, y, label in zip(virginia_cities.geometry.centroid.x, virginia_cities.geometry.centroid.y, virginia_cities['NAME']):
    ax.text(x, y, label, fontsize=6, ha='left', va='top')

# Set plot title
plt.title('Virginia Cities')

# Show the plot

# Save the plot to a PNG file with custom parameters
plt.savefig('D:\Sonal\Documents\GitHub\VaVoterData\VA City Example.png', dpi=900, bbox_inches='tight')
plt.show()

