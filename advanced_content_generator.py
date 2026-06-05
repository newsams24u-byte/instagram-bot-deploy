import os
import anthropic
from typing import Dict, Tuple
import random

class AdvancedContentGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def generate_caption(self, content: Dict) -> Tuple[str, str]:
        """Generate appropriate caption based on content type"""
        
        content_type = content.get("type", "news")
        
        if content_type == "news":
            return self._caption_news(content)
        elif content_type == "weather":
            return self._caption_weather(content)
        elif content_type == "rain_alert":
            return self._caption_rain(content)
        elif content_type == "traffic":
            return self._caption_traffic(content)
        elif content_type == "metro":
            return self._caption_metro(content)
        elif content_type == "poll":
            return self._caption_poll(content)
        elif content_type == "meme":
            return self._caption_meme(content)
        else:
            return self._caption_default(content)
    
    def _caption_news(self, content: Dict) -> Tuple[str, str]:
        """News caption"""
        title = content.get("title", "Breaking News")[:60]
        source = content.get("source", "News Source")
        
        caption = f"📰 BREAKING NEWS!\n\n{title}\n\n"
        caption += "🔗 Swipe up to read full story!\n\n"
        caption += "💬 What's your take? Comment below!\n\n"
        caption += "#BangaloreNews #NewsAlert #BangaloreUpdates #BreakingNews #India"
        
        return caption, title
    
    def _caption_weather(self, content: Dict) -> Tuple[str, str]:
        """Weather caption"""
        temp = content.get("temp", 0)
        condition = content.get("condition", "")
        humidity = content.get("humidity", 0)
        
        emojis = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Thunderstorm": "⛈️",
            "Mist": "🌫️"
        }
        emoji = emojis.get(condition, "🌡️")
        
        caption = f"🌤️ BANGALORE WEATHER UPDATE {emoji}\n\n"
        caption += f"🌡️ Temperature: {temp}°C\n"
        caption += f"💨 Humidity: {humidity}%\n"
        caption += f"Condition: {condition}\n\n"
        caption += "📍 Stay updated with Bangalore weather!\n\n"
        caption += "❓ How's the weather where you are?\n\n"
        caption += "#BangaloreWeather #WeatherUpdate #BangaloreToday #IndiaWeather"
        
        title = f"{condition} - {temp}°C"
        return caption, title
    
    def _caption_rain(self, content: Dict) -> Tuple[str, str]:
        """Rain alert caption"""
        will_rain = content.get("will_rain", False)
        
        if will_rain:
            caption = f"🌧️ RAIN ALERT! ⚠️\n\n"
            caption += f"Looks like rain is coming to Bangalore soon!\n"
            caption += f"Prediction: {content.get('description', 'Rain expected')}\n"
            caption += f"Probability: {content.get('chance', '60%')}\n\n"
            caption += "☔ Remember your umbrella!\n"
            caption += "🚗 Traffic might increase!\n\n"
            caption += "💬 Getting rained in? Tell us your experience!\n\n"
            caption += "#RainAlert #BangaloreRain #BangaloreWeather #MonsoonSeason"
        else:
            caption = "☀️ No rain expected today!\n\n"
            caption += "Perfect day for outdoor plans 🌳\n"
            caption += "Get out and explore Bangalore! 🚴\n\n"
            caption += "💬 What's your plan for today?\n\n"
            caption += "#BangaloreWeather #SunnyDay #BangaloreToday"
        
        title = "Rain Alert ⚠️" if will_rain else "Sunny Day ☀️"
        return caption, title
    
    def _caption_traffic(self, content: Dict) -> Tuple[str, str]:
        """Traffic caption"""
        area = content.get("area", "Bangalore")
        status = content.get("status", "Heavy")
        reason = content.get("reason", "Traffic congestion")
        
        caption = f"🚗 TRAFFIC UPDATE {content.get('emoji', '🚗')}\n\n"
        caption += f"📍 {area}\n"
        caption += f"Status: {status}\n"
        caption += f"Reason: {reason}\n\n"
        caption += "🛣️ Plan your route accordingly!\n"
        caption += "⏰ Leave early or take alternate routes\n\n"
        caption += "💬 Tag your commute struggle! 😩\n\n"
        caption += "#BangaloreTraffic #TrafficUpdate #Bangalore #Commute #RoadToFreedom"
        
        title = f"Traffic Alert: {area}"
        return caption, title
    
    def _caption_metro(self, content: Dict) -> Tuple[str, str]:
        """Metro caption"""
        line = content.get("line", "Metro Line")
        status = content.get("status", "On Time")
        message = content.get("message", "Services normal")
        
        status_emoji = "✅" if status == "On Time" else "⚠️"
        
        caption = f"🚆 BANGALORE METRO {status_emoji}\n\n"
        caption += f"{line}\n"
        caption += f"Status: {status}\n\n"
        caption += f"📢 {message}\n\n"
        caption += "🚇 Best way to beat Bangalore traffic!\n"
        caption += "💰 Affordable & Eco-friendly commute\n\n"
        caption += "💬 What's your favorite metro line?\n\n"
        caption += "#BangaloreMetro #MetroUpdate #BangaloreTransport #CommuteLife"
        
        title = f"Metro: {line} - {status}"
        return caption, title
    
    def _caption_poll(self, content: Dict) -> Tuple[str, str]:
        """Poll caption"""
        question = content.get("question", "What do you prefer?")
        option1 = content.get("option1", "Option 1")
        option2 = content.get("option2", "Option 2")
        option3 = content.get("option3", "Option 3")
        
        caption = f"🗳️ POLL: {question}\n\n"
        caption += f"A. {option1}\n"
        caption += f"B. {option2}\n"
        caption += f"C. {option3}\n\n"
        caption += "💬 Drop your answer in comments!\n"
        caption += "👇 A, B, or C?\n\n"
        caption += "🔄 Tag someone who MUST answer this!\n\n"
        caption += "#BangalorePoll #BangaloreVote #CommunityChoice #YourOpinionMatters"
        
        title = "POLL"
        return caption, title
    
    def _caption_meme(self, content: Dict) -> Tuple[str, str]:
        """Meme caption"""
        caption_text = content.get("caption", "Bangalore Vibes")
        description = content.get("description", "")
        
        caption = f"😂 {caption_text}\n\n"
        caption += f"{description}\n\n"
        caption += "🤣 Tag someone this is about!\n"
        caption += "💬 Can you relate?\n\n"
        caption += "#BangaloreMemes #BangaloreLife #BangaloreHumor #Bangalore #Relatable"
        
        title = caption_text[:40]
        return caption, title
    
    def _caption_default(self, content: Dict) -> Tuple[str, str]:
        """Default caption"""
        caption = "🎯 Bangalore Update\n\n"
        caption += str(content)[:100] + "\n\n"
        caption += "💬 What do you think?\n\n"
        caption += "#Bangalore #BangaloreUpdates"
        
        title = "Bangalore Update"
        return caption, title
    
    def generate_comment_reply(self, comment_text: str, post_type: str) -> str:
        """Generate witty/sensible reply to comment"""
        try:
            prompt = f"""You are a funny, engaging Instagram bot for Bangalore local page. 
A user commented: "{comment_text}"
On a {post_type} post.

Generate a SHORT (1-2 lines max), witty, relatable reply that:
1. Acknowledges their comment
2. Is humorous or encouraging
3. Uses 1-2 relevant emojis
4. Includes a follow-up question or call-to-action
5. Sounds like a real person, not a bot

Keep it under 80 characters!"""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )
            
            reply = message.content[0].text.strip()
            return reply if reply else self._get_fallback_reply(post_type)
        
        except Exception as e:
            print(f"❌ Reply generation error: {e}")
            return self._get_fallback_reply(post_type)
    
    def _get_fallback_reply(self, post_type: str) -> str:
        """Fallback witty replies"""
        replies = {
            "news": "Breaking news breaks our hearts sometimes 😔 But Bangalore keeps moving! 🚀",
            "weather": "Mother Nature can't decide! ☀️🌧️ Classic Bangalore move!",
            "rain_alert": "Umbrella buddies! ☔ Stay safe out there!",
            "traffic": "Traffic is life in Bangalore! We're all warriors 🚗💪",
            "metro": "Metro > Traffic! Smart choice! 🚆✨",
            "poll": "Ooh interesting pick! 👀 We love your style!",
            "meme": "😂 TOO REAL! This is basically Bangalore in a nutshell!"
        }
        return replies.get(post_type, "So true! 💯 Love your energy!")
