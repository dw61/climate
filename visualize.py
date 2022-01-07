import re
import json
import geopandas as gpd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (16, 9)
plt.rcParams["figure.dpi"] = 48
plt.style.use('dark_background')
# plt.rcParams['figure.facecolor'] = 'black'
# plt.rcParams['axes.facecolor'] = 'black'

locations = {}
with open("locations.json", "r") as f:
    locations = json.load(f)

countries = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
usa = countries[countries["name"]=="United States of America"]
bbox = {"boxstyle":"round", "color":"black", "alpha":0.4}

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

    fig, ax = plt.subplots(1, 1)
    usa.plot(color="lightblue", ax=ax)
    sp = ax.scatter(longitudes, latitudes, c=colors, cmap=cmap, s=200)
    ax.annotate("New York", (-73.974304, 40.779249), ha="center", bbox=bbox)
    ax.annotate("Los Angeles", (-118.242766, 34.053691), ha="center", bbox=bbox)
    ax.annotate("Chicago", (-87.624421, 41.875562), ha="center", bbox=bbox)
    ax.annotate("Houston", (-95.367697, 29.758938), ha="center", bbox=bbox)
    ax.annotate("Seattle", (-122.330062, 47.603832), ha="center", bbox=bbox)
    ax.annotate("Miami", (-80.19362, 25.774173), ha="center", bbox=bbox)
    ax.annotate("Anchorage", (-149.894852, 61.216313), ha="center", bbox=bbox)
    ax.annotate("Honolulu", (-157.855676, 21.304547), ha="center", bbox=bbox)
    fig.colorbar(sp)
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    fig.savefig(f"figures/{figurefile}")

plot("clpcdy18.dat", "1_cloud.png", "Number of Cloudy Days in a Year")
plot("prge0118.dat", "2_rain.png", "Number of Precipitation Days in a Year")
plot("avgsnf18.dat", "3_snow.png", "Yearly Snow Fall (inch)")
plot("relhum18.dat", "4_humidity.png", "Relative Afternoon Humidity")
plot("wndspd18.dat", "5_wind.png", "Average Wind Speed (mph)")
plot("mnls3218.dat", "6_cold.png", "Number of Cold (<32F) Days")
plot("mxge9018.dat", "7_hot.png", "Number of Hot (>90F) Days", cmap="summer_r")
plot("hghtmp18.dat", "8_record_high.png", "Record High Temperature (F)", cmap="viridis")
plot("nrmmax.txt", "9_mean_maximum.png", "Mean Maximum Temperature (F)", cmap="viridis")
plot("nrmavg.txt", "10_average.png", "Average Temperature (F)", cmap="viridis")
plot("nrmmin.txt", "11_mean_minimum.png", "Mean Minimum Temperature (F)", cmap="viridis")
plot("lowtmp18.dat", "12_record_low.png", "Record Low Temperature (F)", cmap="viridis")
plot("pctpos18.dat", "13_sunshine.png", "Percentage Sunshine of Possible", cmap="viridis")
plot("nrmpcp.txt", "14_precipitation.png", "Yearly Precipitation (inch)")
