import csv
from datetime import datetime
import matplotlib.pyplot as plt

# Data structure to hold city-wise data
city_data = {}

with open('weather_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')

            if len(row) == 3:
                city = row[1]
                weather_info = row[2]
            elif len(row) == 2:
                # city and weather merged, try to split at first colon
                city_weather = row[1]
                city, weather_info = city_weather.split(':', 1)
                city = city.strip()
                weather_info = weather_info.strip()
            else:
                continue

            temp_str = weather_info.split()[-1].replace("°C", "")
            temperature = int(temp_str)

            if city not in city_data:
                city_data[city] = {'timestamps': [], 'temperatures': []}

            city_data[city]['timestamps'].append(timestamp)
            city_data[city]['temperatures'].append(temperature)

        except Exception as e:
            print(f"Skipping row due to error: {e}, row: {row}")
            continue

plt.figure(figsize=(12, 6))

for city, data in city_data.items():
    plt.plot(data['timestamps'], data['temperatures'], marker='o', label=city)

plt.title('Temperature Trends Over Time by City')
plt.xlabel('Date & Time')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
