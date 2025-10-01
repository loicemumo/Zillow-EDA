#Import libraries
import requests
import pandas as pd
import json
from datetime import datetime

#Load API keys from config.json
with open("config.json", "r") as f:
    config = json.load(f)

headers = {
    "x-rapidapi-key": config["x-rapidapi-key"],
    "x-rapidapi-host": config["x-rapidapi-host"]
}

#List of cities to loop through
cities = [
    "houston, tx",
    "dallas, tx",
    "austin, tx",
    "san antonio, tx",
    "chicago, il",
    "los angeles, ca",
    "new york, ny",
    "miami, fl",
    "phoenix, az",
    "seattle, wa"
]
url = "https://zillow56.p.rapidapi.com/search"

all_properties = []

for city in cities:
    print(f"📡 Fetching data for {city}...")
    
    params = {
        "location": city,
        "output": "json",
        "status": "forSale",
        "sortSelection": "priorityscore",
        "listing_type": "by_agent",
        "doz": "any"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        properties = data.get("results", [])

        for prop in properties:
            prop["city"] = city  # add city column
            all_properties.append(prop)

        print(f"✅ {len(properties)} properties fetched from {city}")

    else:
        print(f"❌ Failed for {city} - status {response.status_code}")

#Convert everything into a DataFrame
df = pd.DataFrame(all_properties)

# Save to CSV with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = f"zillow_all_cities_{timestamp}.csv"
df.to_csv(csv_file, index=False, encoding="utf-8")

print(f"\n🎉 All data saved to {csv_file}")
print(f"Total rows: {len(df)}")