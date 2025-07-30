import requests
import csv
import os
from datetime import datetime

API_KEY = "8544f8218d68a0ade388e2986e4359bb"  # Example API key

def fetch_weather(city: str, api_key: str) -> dict:

    # Fetch weather data for a given city using OpenWeatherMap API

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'  # For Celsius
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise ValueError(f"City '{city}' not found. Please check the spelling.")
        elif response.status_code == 401:
            raise ValueError("Invalid API key. Please check your OpenWeatherMap API key.")
        else:
            raise Exception(f"API request failed with status code {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Network error. Please check your internet connection.")
    except requests.exceptions.Timeout:
        raise TimeoutError("Request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred while fetching weather: {e}")
    except Exception as e:
        raise e

def analyze_weather(weather_data: dict) -> tuple:

    # Analyze weather data and return temperature category and warnings
    # Returns: (temperature_category, warnings_list)

    try:
        temp = weather_data['main']['temp']
        
        if temp <= 15:
            temp_category = "Cold"
        elif temp <= 29:
            temp_category = "Mild"
        else:
            temp_category = "Hot"
        
        warnings = []
        
        wind_speed = weather_data.get('wind', {}).get('speed', 0)
        if wind_speed > 10:
            warnings.append("High wind alert!")
        
        humidity = weather_data['main']['humidity']
        if humidity > 80:
            warnings.append("Humid conditions!")
        
        return temp_category, warnings
        
    except KeyError as e:
        raise Exception(f"Missing weather data field: {e}")
    except Exception as e:
        raise Exception(f"Error analyzing weather: {e}")

def log_weather(city: str, api_key: str, filename: str = "weather_log.csv"):

    # Fetch weather for city and append data to CSV file

    try:
        weather_data = fetch_weather(city, api_key)
        temp_category, warnings = analyze_weather(weather_data)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            'timestamp': timestamp,
            'city': weather_data['name'],
            'country': weather_data['sys']['country'],
            'temperature': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'humidity': weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            'wind_speed': weather_data.get('wind', {}).get('speed', 'N/A'),
            'description': weather_data['weather'][0]['description'],
            'temp_category': temp_category,
            'warnings': '; '.join(warnings) if warnings else 'None'
        }
        
        file_exists = os.path.exists(filename)
        
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = list(data.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
                
            writer.writerow(data)
        
        return weather_data, temp_category, warnings
        
    except Exception as e:
        raise Exception(f"Error logging weather: {e}")

def display_weather_info(weather_data: dict, temp_category: str, warnings: list):

    # Display formatted weather information

    print("\n" + "="*50)
    print("WEATHER INFORMATION")
    print("="*50)
    print(f"Location: {weather_data['name']}, {weather_data['sys']['country']}")
    print(f"Temperature: {weather_data['main']['temp']:.1f}°C")
    print(f"Feels like: {weather_data['main']['feels_like']:.1f}°C")
    print(f"Condition: {weather_data['weather'][0]['description'].title()}")
    print(f"Humidity: {weather_data['main']['humidity']}%")
    print(f"Pressure: {weather_data['main']['pressure']} hPa")
    wind_speed = weather_data.get('wind', {}).get('speed', 'N/A')
    print(f"Wind Speed: {wind_speed} m/s" if wind_speed != 'N/A' else "Wind Speed: N/A")
    print(f"Category: {temp_category}")
    
    if warnings:
        print("\n⚠️ WARNINGS:")
        for warning in warnings:
            print(f"  • {warning}")
    else:
        print("\n✅ No warnings")
        
    print("="*50)

def main():
    print("Weather Data Fetcher & Analyzer")
    print("="*40)
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️ Please set your OpenWeatherMap API key in the code!")
        print("   Get your free API key at: https://openweathermap.org/api")
        return
    
    try:
        city = input("Enter city name: ").strip()
        if not city:
            print("Error: Please enter a city name.")
            return
        
        print(f"\nFetching weather data for {city}...")
        weather_data, temp_category, warnings = log_weather(city, API_KEY)
        display_weather_info(weather_data, temp_category, warnings)
        print(f"\n✅ Weather data saved to 'weather_log.csv'")
        
    except ValueError as e:
        print(f"❌ Input Error: {e}")
    except ConnectionError as e:
        print(f"❌ Network Error: {e}")
    except TimeoutError as e:
        print(f"❌ Timeout Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
