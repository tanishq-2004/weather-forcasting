import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import joblib
import numpy as np

# Load the trained model
model = joblib.load("weather_prediction_model.pkl")

def get_weather_data(city):
    """Fetches weather data for a given city using OpenWeatherMap API."""
    api_key = "b845409c0cacbb1860f1b8ce1da36909"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"⚠️ Unable to fetch weather for {city}!\nReason: {e}")
        return None

def predict_weather(temp, humidity, wind_speed):
    """Predicts future weather conditions using the trained model."""
    features = np.array([[temp, humidity, wind_speed]])
    prediction = model.predict(features)
    prediction_map = {0: "Sunny", 1: "Rainy", 2: "Snowy"}
    return prediction_map.get(prediction[0], "Unknown")

def display_weather_info(data):
    """Displays weather information, including predictions."""
    if data:
        city = data.get("name", "Unknown City")
        temp = data.get("main", {}).get("temp", "N/A")
        humidity = data.get("main", {}).get("humidity", "N/A")
        wind_speed = data.get("wind", {}).get("speed", "N/A")
        weather = data.get("weather", [{}])[0].get("description", "N/A")
        timestamp = data.get("dt", None)
        date_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        # Predict weather condition using the trained model
        predicted_condition = predict_weather(temp, humidity, wind_speed)

        messagebox.showinfo("🌟 Weather Wizard Update 🌟", 
            f"✨ Here's the latest forecast! ✨\n\n"
            f"📍 Location: {city}\n"
            f"🕒 Date & Time: {date_time}\n"
            f"🌡️ Temperature: {temp}°C\n"
            f"💧 Humidity: {humidity}%\n"
            f"🍃 Wind Speed: {wind_speed} m/s\n"
            f"☁️ Current Condition: {weather.capitalize()}\n\n"
            f"🔮 Predicted Future Condition: {predicted_condition}\n\n"
            f"🌈 Stay safe and enjoy your day! 🌈")
    else:
        messagebox.showerror("No Data", "🚨 Oops! Couldn't retrieve the weather. Please try again! 🚨")

def on_check_weather():
    city = city_entry.get()
    if city:
        weather_data = get_weather_data(city)
        display_weather_info(weather_data)
    else:
        messagebox.showwarning("Input Error", "❗ Please enter a city name!")

def main():
    """Main function to create the GUI for the Weather App."""
    global city_entry

    root = tk.Tk()
    root.title("🌤️ Weather Wizard App 🌤️")
    root.configure(bg="#9370DB")  # Light violet background

    tk.Label(root, text="🌤️ Welcome to the Weather Wizard App! 🌤️", font=("Comic Sans MS", 16), bg="#9370DB", fg="white").pack(pady=10)

    tk.Label(root, text="🗺️ Enter the name of a city:", font=("Comic Sans MS", 12), bg="#9370DB", fg="white").pack(pady=5)
    city_entry = tk.Entry(root, width=30, font=("Comic Sans MS", 12))
    city_entry.pack(pady=5)

    tk.Button(root, text="🔍 Get Weather", command=on_check_weather, font=("Comic Sans MS", 12), bg="#6A5ACD", fg="white", padx=10, pady=5).pack(pady=10)

    tk.Label(root, text="✨ Powered by OpenWeatherMap ✨", font=("Comic Sans MS", 10), bg="#9370DB", fg="white").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
