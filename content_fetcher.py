import requests
import os
import random
from typing import List, Dict
from datetime import datetime

class ContentFetcher:
    def __init__(self):
        self.newsapi_key = os.getenv("NEWSAPI_KEY")
        self.weather_key = os.getenv("OPENWEATHER_API_KEY")
        self.bangalore_lat = float(os.getenv("BANGALORE_LAT", 12.9716))
        self.bangalore_lng = float(os.getenv("BANGALORE_LNG", 77.5946))
    
    # ======================== NEWS ========================
    def get_bangalore_news(self) -> Dict:
        """Fetch Bangalore news"""
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": "Bangalore OR Bengaluru",
                "sortBy": "publishedAt",
                "language": "en",
                "apiKey": self.newsapi_key,
                "pageSize": 5
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                if articles:
                    return {
                        "type": "news",
                        "title": articles[0].get("title", ""),
                        "description": articles[0].get("description", ""),
                        "source": articles[0].get("source", {}).get("name", "News"),
                        "url": articles[0].get("url", "")
                    }
        except Exception as e:
            print(f"❌ News fetch error: {e}")
        return None
    
    # ======================== WEATHER ========================
    def get_bangalore_weather(self) -> Dict:
        """Fetch current Bangalore weather"""
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "lat": self.bangalore_lat,
                "lon": self.bangalore_lng,
                "appid": self.weather_key,
                "units": "metric"
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "type": "weather",
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "condition": data["weather"][0]["main"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "rain_mm": data.get("rain", {}).get("1h", 0)
                }
        except Exception as e:
            print(f"❌ Weather fetch error: {e}")
        return None
    
    # ======================== RAIN ALERTS ========================
    def get_rain_alert(self) -> Dict:
        """Check if rain is expected"""
        try:
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {
                "lat": self.bangalore_lat,
                "lon": self.bangalore_lng,
                "appid": self.weather_key,
                "units": "metric",
                "cnt": 8  # Next 24 hours
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                forecasts = response.json().get("list", [])
                rain_forecasts = [f for f in forecasts if f["weather"][0]["main"] in ["Rain", "Thunderstorm"]]
                
                if rain_forecasts:
                    first_rain = rain_forecasts[0]
                    return {
                        "type": "rain_alert",
                        "will_rain": True,
                        "description": first_rain["weather"][0]["description"],
                        "time": first_rain["dt_txt"],
                        "chance": f"{int(first_rain['pop'] * 100)}%"
                    }
                else:
                    return {
                        "type": "rain_alert",
                        "will_rain": False,
                        "description": "Clear skies ahead ☀️"
                    }
        except Exception as e:
            print(f"❌ Rain alert error: {e}")
        return None
    
    # ======================== TRAFFIC & METRO ========================
    def get_bangalore_traffic(self) -> Dict:
        """Generate Bangalore traffic update"""
        hot_spots = [
            {"area": "Silk Board", "status": "Heavy", "emoji": "🚗🚗🚗", "reason": "Construction work"},
            {"area": "Whitefield", "status": "Moderate", "emoji": "🚗🚗", "reason": "Peak hours"},
            {"area": "MG Road", "status": "Heavy", "emoji": "🚗🚗🚗", "reason": "Shopping traffic"},
            {"area": "Koramangala", "status": "Light", "emoji": "🚗", "reason": "Normal flow"},
            {"area": "Indiranagar", "status": "Moderate", "emoji": "🚗🚗", "reason": "Evening rush"},
            {"area": "Sarjapur Road", "status": "Heavy", "emoji": "🚗🚗🚗", "reason": "Tech park traffic"},
            {"area": "Hebbal", "status": "Moderate", "emoji": "🚗🚗", "reason": "Normal congestion"},
        ]
        
        selected = random.choice(hot_spots)
        return {
            "type": "traffic",
            "area": selected["area"],
            "status": selected["status"],
            "emoji": selected["emoji"],
            "reason": selected["reason"]
        }
    
    def get_bangalore_metro(self) -> Dict:
        """Bangalore Metro updates"""
        updates = [
            {
                "line": "Purple Line",
                "status": "On Time",
                "message": "All services running normally. Expected wait time: 5-7 mins"
            },
            {
                "line": "Green Line",
                "status": "Delayed",
                "message": "Minor delay due to higher passenger volume. ~15 mins wait"
            },
            {
                "line": "Red Line",
                "status": "On Time",
                "message": "Services operating smoothly. Enjoy your commute! 🚆"
            },
            {
                "line": "Blue Line",
                "status": "On Time",
                "message": "All stations operational. No delays reported"
            },
        ]
        selected = random.choice(updates)
        return {
            "type": "metro",
            **selected
        }
    
    # ======================== POLLS ========================
    def get_poll_post(self) -> Dict:
        """Generate poll-style post"""
        polls = [
            {
                "question": "Best time to visit Bangalore? ☀️",
                "option1": "Winter (Oct-Jan) 🧊",
                "option2": "Summer (Mar-May) 🔥",
                "option3": "Monsoon (Jun-Sep) 🌧️"
            },
            {
                "question": "Favorite Bangalore munchies? 🍔",
                "option1": "Filter Coffee ☕",
                "option2": "Dosa 🫓",
                "option3": "Biryani 🍚"
            },
            {
                "question": "Most annoying in Bangalore traffic? 🚗",
                "option1": "Autos ignoring signals 🚛",
                "option2": "Lane cutting 😤",
                "option3": "Honking constantly 🔊"
            },
            {
                "question": "Best Bangalore IT park? 🏢",
                "option1": "Whitefield 🌟",
                "option2": "Sarjapur 💼",
                "option3": "MG Road 🏙️"
            },
        ]
        selected = random.choice(polls)
        return {
            "type": "poll",
            **selected
        }
    
    # ======================== MEMES ========================
    def get_bangalore_meme(self) -> Dict:
        """Bangalore local meme generator"""
        memes = [
            {
                "caption": "When you say 'traffic' in Bangalore",
                "description": "Me: I'll be there in 10 mins\nReality: 45 mins later..."
            },
            {
                "caption": "Bangalore vs Monsoon",
                "description": "1 drop of rain = All flooding\n1 degree temperature drop = Everyone buying sweaters 🧥"
            },
            {
                "caption": "Every Bangalorean planning weekend",
                "description": "Weekend plan: Visit Cubbon Park\nActual: Sitting in traffic to Cubbon Park"
            },
            {
                "caption": "Bangalore Metro experience",
                "description": "Expected: Smooth commute\nReality: Sardine can with human filling 🚆"
            },
            {
                "caption": "Tech park culture",
                "description": "Monday: Fresh and energetic\nWednesday: Dead inside\nFriday: Waiting for the weekend"
            },
            {
                "caption": "Bangalore vs Other Cities",
                "description": "Other cities: Normal weather\nBangalore: WEATHER DECIDE KARO! 🌤️🌧️"
            },
        ]
        selected = random.choice(memes)
        return {
            "type": "meme",
            **selected
        }
    
    # ======================== MAIN SELECTOR ========================
    def get_random_content(self) -> Dict:
        """Get random content type"""
        content_types = [
            self.get_bangalore_news,
            self.get_bangalore_weather,
            self.get_rain_alert,
            self.get_bangalore_traffic,
            self.get_bangalore_metro,
            self.get_poll_post,
            self.get_bangalore_meme,
        ]
        
        for attempt in range(3):
            selector = random.choice(content_types)
            result = selector()
            if result:
                return result
        
        # Fallback
        return self.get_bangalore_meme()
