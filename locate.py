from tqdm import tqdm
import json
import geopy
geolocator = geopy.geocoders.Nominatim(user_agent="cloudy")

locations = {}
failed = set()

def locate(filename, header=1):

    with open(f"data/{filename}", "r") as f:
        lines = f.read().split('\n')[header:-1]

    pbar = tqdm(lines, bar_format="{n_fmt:>3}/{total_fmt}|{bar}{desc:>16} ")
    for line in pbar:

        zipcode = line[:5]
        if zipcode in locations or zipcode in failed:
            continue

        city, state = line[5:37].split(",")
        city = city.replace(" AP", "").strip()
        state = state.strip()
        pbar.set_description_str(f"{city}, {state}")

        location = geolocator.geocode(f"{city}, {state}", timeout=3)
        if location and "United States" in location.address:
            locations[zipcode] = [city, state, location.longitude, location.latitude]
        else:
            failed.add(zipcode)

locate("avgsnf18.dat")
locate("clpcdy18.dat", header=2)
locate("nrmmin.txt")

with open("locations.json", "w") as f:
    json.dump(locations, f)
