import re
import json
import geopandas as gpd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (16, 9)
plt.rcParams["figure.dpi"] = 240
plt.rcParams['figure.facecolor'] = 'pink'
plt.rcParams['axes.facecolor'] = 'pink'

locations = {}
with open("locations.json", "r") as f:
    locations = json.load(f)

countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
usa = countries[countries["name"]=="United States of America"]
bbox = {"boxstyle":"round", "color":"white", "alpha":0.4}

def plot(datafile, figurefile, title, cmap="viridis_r"):

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

    usa.plot(color="lightblue")
    plt.scatter(longitudes, latitudes, c=colors, cmap=cmap, s=200)
    plt.annotate("New York", (-73.974304, 40.779249), ha="center", bbox=bbox)
    plt.annotate("Los Angeles", (-118.242766, 34.053691), ha="center", bbox=bbox)
    plt.annotate("Chicago", (-87.624421, 41.875562), ha="center", bbox=bbox)
    plt.annotate("Houston", (-95.367697, 29.758938), ha="center", bbox=bbox)
    plt.annotate("Seattle", (-122.330062, 47.603832), ha="center", bbox=bbox)
    plt.annotate("Miami", (-80.19362, 25.774173), ha="center", bbox=bbox)
    plt.annotate("Anchorage", (-149.894852, 61.216313), ha="center", bbox=bbox)
    plt.annotate("Honolulu", (-157.855676, 21.304547), ha="center", bbox=bbox)
    plt.colorbar()
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig(f"figures/{figurefile}", bbox_inches='tight')

plot("clpcdy18.dat", "1 cloud.png", "Number of Cloudy Days in a Year")
plot("prge0118.dat", "2 rain.png", "Number of Precipitation Days in a Year")
plot("avgsnf18.dat", "3 snow.png", "Yearly Snow Fall (inch)")
plot("relhum18.dat", "4 humidity.png", "Relative Afternoon Humidity")
plot("wndspd18.dat", "5 wind.png", "Average Wind Speed (mph)")
plot("mnls3218.dat", "6 cold.png", "Number of Cold (<32F) Days")
plot("mxge9018.dat", "7 hot.png", "Number of Hot (>90F) Days", cmap="summer_r")
plot("hghtmp18.dat", "8 record high.png", "Record High Temperature (F)", cmap="viridis")
plot("nrmmax.txt", "9 mean maximum.png", "Mean Maximum Temperature (F)", cmap="viridis")
plot("nrmavg.txt", "10 average.png", "Average Temperature (F)", cmap="viridis")
plot("nrmmin.txt", "11 mean minimum.png", "Mean Minimum Temperature (F)", cmap="viridis")
plot("lowtmp18.dat", "12 record low.png", "Record Low Temperature (F)", cmap="viridis")
plot("pctpos18.dat", "13 sunshine.png", "Percentage Sunshine of Possible", cmap="viridis")
plot("nrmpcp.txt", "14 precipitation.png", "Yearly Precipitation (inch)")
