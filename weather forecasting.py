import requests
import tkinter as tk
from tkinter import messagebox

def get_weather_data(city):
    """Fetches weather data for a given city using OpenWeatherMap API."""
    api_key = "b845409c0cacbb1860f1b8ce1da36909" 
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
        messagebox.showerror("Error", f"Oops! Couldn't fetch the weather for {city}. Reason: {e}")
        return None

def display_weather_info(data):
    """Displays weather information in a creative way."""
    if data:
        city = data.get("name", "Unknown City")
        country = data.get("sys", {}).get("country", "Unknown Country")
        temp = data.get("main", {}).get("temp", "N/A")
        weather = data.get("weather", [{}])[0].get("description", "N/A")

        messagebox.showinfo("Weather Update", 
            f"🌟 Here's your weather update! 🌟\n\n"
            f"📍 Location: {city}, {country}\n"
            f"🌡️ Temperature: {temp}°C\n"
            f"☁️ Condition: {weather.capitalize()}\n\n"
            f"Stay prepared and have a wonderful day! 🌈")
    else:
        messagebox.showerror("No Data", "🚨 No weather data available. Please try again. 🚨")

def on_check_weather():
    city = city_entry.get()
    if city:
        weather_data = get_weather_data(city)
        display_weather_info(weather_data)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name.")

def main():
    """Main function to create the GUI for the Weather App."""
    global city_entry

    root = tk.Tk()
    root.title("Weather Wizard App")

    tk.Label(root, text="🌤️ Welcome to the Weather Wizard App! 🌤️", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="🗺️ Enter the name of a city:", font=("Arial", 12)).pack(pady=5)
    city_entry = tk.Entry(root, width=30, font=("Arial", 12))
    city_entry.pack(pady=5)

    tk.Button(root, text="Get Weather", command=on_check_weather, font=("Arial", 12), bg="blue", fg="white").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
