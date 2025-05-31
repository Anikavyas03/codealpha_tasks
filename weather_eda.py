import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Load raw CSV as one column, since delimiters vary
df_raw = pd.read_csv("weather_data.csv", header=None, names=["raw"])

# Split 'raw' into timestamp and rest by first comma
df_raw[['timestamp', 'rest']] = df_raw['raw'].str.split(',', 1, expand=True)

# Extract city and weather info from 'rest'
def clean_city_weather(text):
    # Remove duplicate city if repeated, e.g., "Bhopal,Bhopal: ☀️ +30°C"
    # Split by comma first
    parts = text.split(',')
    if len(parts) == 2:
        city = parts[0].strip()
        weather_info = parts[1].strip()
    else:
        # If no extra comma, then split by colon
        city, weather_info = text.split(':', 1)
        city = city.strip()
        weather_info = weather_info.strip()
    return city, weather_info

df_raw[['city', 'weather_info']] = df_raw['rest'].apply(lambda x: pd.Series(clean_city_weather(x)))

# Extract temperature and condition (emoji)
def parse_weather(info):
    try:
        # Extract temperature using regex (e.g. +32°C or -5°C)
        temp_match = re.search(r'([+-]?\d+)°C', info)
        temp = int(temp_match.group(1)) if temp_match else None

        # Extract emoji (unicode weather icon) - first non-space char
        condition_match = re.match(r'(\W+)', info)  # non-word chars at start
        condition = condition_match.group(1).strip() if condition_match else "Unknown"
        return pd.Series([temp, condition])
    except:
        return pd.Series([None, None])

df_raw[['temperature', 'condition']] = df_raw['weather_info'].apply(parse_weather)

# Convert timestamp to datetime
df_raw["timestamp"] = pd.to_datetime(df_raw["timestamp"])

# Drop unnecessary columns
df = df_raw.drop(columns=["raw", "rest"])

# Display cleaned data sample
print("Cleaned Data Sample:")
print(df.head())

# Basic EDA
print("\nAverage Temperature by City:")
print(df.groupby("city")["temperature"].mean())

print("\nWeather Condition Counts:")
print(df["condition"].value_counts())

# Visualization setup
sns.set(style="whitegrid")

# 1. Average Temperature by City (Bar plot)
plt.figure(figsize=(8,5))
sns.barplot(x="city", y="temperature", data=df, ci=None, palette="coolwarm")
plt.title("Average Temperature by City")
plt.ylabel("Temperature (°C)")
plt.xlabel("City")
plt.show()

# 2. Weather Condition Counts (Bar plot)
plt.figure(figsize=(8,5))
sns.countplot(y="condition", data=df, order=df["condition"].value_counts().index, palette="viridis")
plt.title("Weather Condition Counts")
plt.xlabel("Count")
plt.ylabel("Condition")
plt.show()

# 3. Temperature over Time for each City (Line plot)
plt.figure(figsize=(10,6))
sns.lineplot(data=df, x="timestamp", y="temperature", hue="city", marker="o")
plt.title("Temperature Over Time by City")
plt.ylabel("Temperature (°C)")
plt.xlabel("Timestamp")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
