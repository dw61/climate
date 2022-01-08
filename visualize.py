import re
import json
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import ticker
plt.rcParams["figure.figsize"] = (16, 9)
plt.rcParams["figure.dpi"] = 480
plt.rcParams["font.family"] = "American Typewriter"
plt.style.use('dark_background')

locations = {}
with open("locations.json", "r") as f:
    locations = json.load(f)

# countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
# usa = countries[countries["name"]=="United States of America"]
usa = gpd.read_file("usa/usa-states-census-2014.shp")
usa.to_crs("EPSG:3395")
annotation = {"ha":"center", "bbox":{"boxstyle":"round", "color":"black", "alpha":0.4}}

def plot(datafile, figurefile, title, unit="", cmap="viridis_r"):

    with open(f"data/{datafile}", "r") as f:
        lines = f.read().split('\n')

    longitudes = []
    latitudes = []
    colors = []

    for c in lines[:-1]:
        zipcode = c[:5]
        climate = re.split(", *| +", c[37:])

        if zipcode in locations:
            location = locations[zipcode]
            longitudes.append(location[2])
            latitudes.append(location[3])
            colors.append(float(climate[-1]))

    usa.plot(color="lightblue", edgecolor="black", linewidth=0.3)
    plt.scatter(longitudes, latitudes, c=colors, cmap=cmap, s=600)
    cbar = plt.colorbar(format=lambda x, _ : f"{x:0g} {unit}", shrink=0.80, pad=0.02)
    cbar.outline.set_visible(False)
    cbar.ax.locator_params(nbins=6)

    plt.annotate("New York", (-73.974304, 40.779249), **annotation)
    plt.annotate("Los Angeles", (-118.242766, 34.053691), **annotation)
    plt.annotate("Chicago", (-87.624421, 41.875562), **annotation)
    plt.annotate("Houston", (-95.367697, 29.758938), **annotation)
    plt.annotate("Seattle", (-122.330062, 47.603832), **annotation)
    plt.annotate("Miami", (-80.19362, 25.774173), **annotation)
    plt.annotate("Anchorage", (-149.894852, 61.216313), **annotation)
    plt.annotate("Honolulu", (-157.855676, 21.304547), **annotation)
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig(f"figures/{figurefile}")

plot("clpcdy18.dat", "1_cloud.png", "Number of Cloudy Days in a Year", "days")
plot("prge0118.dat", "2_rain.png", "Number of Precipitation Days in a Year", "days")
plot("avgsnf18.dat", "3_snow.png", "Yearly Snow Fall", "in")
plot("relhum18.dat", "4_humidity.png", "Relative Afternoon Humidity", "%")
plot("wndspd18.dat", "5_wind.png", "Average Wind Speed", "mph")
plot("mnls3218.dat", "6_cold.png", "Number of Cold (<32F) Days", "days")
plot("mxge9018.dat", "7_hot.png", "Number of Hot (>90F) Days", "days", "summer_r")
plot("hghtmp18.dat", "8_record_high.png", "Record High Temperature", "\u00B0F", "viridis")
plot("nrmmax.txt", "9_mean_maximum.png", "Mean Maximum Temperature", "\u00B0F", "viridis")
plot("nrmavg.txt", "10_average.png", "Average Temperature", "\u00B0F", "viridis")
plot("nrmmin.txt", "11_mean_minimum.png", "Mean Minimum Temperature", "\u00B0F", "viridis")
plot("lowtmp18.dat", "12_record_low.png", "Record Low Temperature", "\u00B0F", "viridis")
plot("pctpos18.dat", "13_sunshine.png", "Percentage Sunshine of Possible", "%", "viridis")
plot("nrmpcp.txt", "14_precipitation.png", "Yearly Precipitation", "in")
