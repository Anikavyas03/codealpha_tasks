import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

cities = ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain"]

with open("weather_data.csv", mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    for city in cities:
        print(f"\nFetching weather for {city}...")
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url)

        if response.status_code == 200:
            weather_info = response.text.strip()

            print("✓", weather_info)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([now, city, weather_info])
            print("Saved to CSV ✅")

        else:
            print(f"Failed to get weather for {city}, Status code:", response.status_code)







