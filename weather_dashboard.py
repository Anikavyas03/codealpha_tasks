import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

st.title("Weather Data Dashboard - MP Cities")

@st.cache_data
def load_data():
    city_data = {}
    with open('weather_data.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        row = line.strip().split(',', 2)
        try:
            timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            if len(row) == 3:
                city = row[1]
                weather_info = row[2]
            elif len(row) == 2:
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
        except:
            continue

    return city_data

city_data = load_data()
cities = list(city_data.keys())

view_option = st.radio("Choose View:", ("All Cities", "Single City"))

if view_option == "Single City":
    selected_city = st.selectbox("Select City", cities)
    data = city_data[selected_city]

    plt.figure(figsize=(10, 5))
    plt.plot(data['timestamps'], data['temperatures'], marker='o', linestyle='-', label=selected_city)
    plt.title(f"Temperature Trend for {selected_city}")
    plt.xlabel("Date & Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)

    if st.checkbox("Show Raw Data for Selected City"):
        df = pd.DataFrame({
            "Timestamp": data['timestamps'],
            "Temperature (°C)": data['temperatures']
        })
        st.dataframe(df)

else:
    plt.figure(figsize=(12, 6))
    for city in cities:
        data = city_data[city]
        plt.plot(data['timestamps'], data['temperatures'], marker='o', linestyle='-', label=city)

    plt.title("Temperature Trends for All Cities")
    plt.xlabel("Date & Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)

    if st.checkbox("Show Raw Data for All Cities"):
        # Combine all city data into one dataframe
        records = []
        for city in cities:
            for t, temp in zip(city_data[city]['timestamps'], city_data[city]['temperatures']):
                records.append({"City": city, "Timestamp": t, "Temperature (°C)": temp})
        df_all = pd.DataFrame(records)
        st.dataframe(df_all)
