import csv

with open("weather_data.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    headers = next(reader)
    print("CSV Headers:", headers)
