import requests
import json
from datetime import datetime

def get_weather_simple(city):
    """Simple weather — ek line mein"""
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=3",
            timeout=5
        )
        if response.status_code == 200:
            return response.text.strip()
        else:
            return None
    except:
        return None

def get_weather_detailed(city):
    """Detailed weather — JSON format mein"""
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=j1",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            
            current = data["current_condition"][0]
            
            temp = current["temp_C"]
            feels_like = current["FeelsLikeC"]
            humidity = current["humidity"]
            description = current["weatherDesc"][0]["value"]
            wind = current["windspeedKmph"]
            
            return {
                "temp": temp,
                "feels_like": feels_like,
                "humidity": humidity,
                "description": description,
                "wind": wind
            }
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_search(city, weather_info):
    """Search history save karo"""
    try:
        with open("weather_history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    
    history.append({
        "city": city,
        "weather": weather_info,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    
    with open("weather_history.json", "w") as f:
        json.dump(history, f, indent=4)

def show_history():
    """Purani searches dikho"""
    try:
        with open("weather_history.json", "r") as f:
            history = json.load(f)
        
        if not history:
            print("Koi history nahi!")
            return
            
        print("\n--- Tumhari Search History ---")
        for item in history:
            print(f"{item['time']} | {item['city']} | {item['weather']['description']}, {item['weather']['temp']}°C")
    except FileNotFoundError:
        print("Koi history nahi abhi tak!")

# ==================
# MAIN PROGRAM
# ==================

print("🌤️  Weather App — Powered by Python")
print("=" * 40)

while True:
    print("\n1. Kisi city ka weather dekho")
    print("2. Search history dekho")
    print("3. Quit")
    
    choice = input("\nOption: ")
    
    if choice == "1":
        city = input("City ka naam: ")
        
        print(f"\n🔍 {city} ka weather dhundh raha hun...")
        
        weather = get_weather_detailed(city)
        
        if weather:
            print(f"\n🌡️  Temperature:  {weather['temp']}°C")
            print(f"🤔 Feels Like:   {weather['feels_like']}°C")
            print(f"💧 Humidity:     {weather['humidity']}%")
            print(f"💨 Wind Speed:   {weather['wind']} km/h")
            print(f"☁️  Condition:    {weather['description']}")
            
            save_search(city, weather)
            print("\n✅ Search history mein save ho gaya!")
        else:
            print("❌ Weather nahi mila — city ka naam check karo!")
    
    elif choice == "2":
        show_history()
    
    elif choice == "3":
        print("Khuda Hafiz! ☀️")
        break
    
    else:
        print("❌ Galat option!")