
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import re

data = {}

with open("weather_data.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        # Check row length
        if len(row) < 3:
            continue  # skip malformed rows

        timestamp_str = row[0]
        city = row[1].strip()
        city_weather = row[2].strip()

        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except:
            continue  # skip if timestamp is invalid

        # Extract temperature in Celsius
        temp_match = re.search(r"([+-]?\d+)°C", city_weather)
        if temp_match:
            temp = int(temp_match.group(1))
        else:
            temp = None

        if temp is not None:
            if city not in data:
                data[city] = {"timestamps": [], "temps": []}
            data[city]["timestamps"].append(timestamp)
            data[city]["temps"].append(temp)

# Plotting
plt.figure(figsize=(10, 6))

for city, values in data.items():
    plt.plot(values["timestamps"], values["temps"], marker='o', label=city)

plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Trends by City")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
