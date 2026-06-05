import os
from PIL import Image, ImageDraw, ImageFont
import random
from typing import Dict

class AdvancedImageCreator:
    def __init__(self, width: int = 1080, height: int = 1350):
        self.width = width
        self.height = height
        self.output_dir = "instagram_agent/posts"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_image(self, content: Dict) -> str:
        """Create image based on content type"""
        content_type = content.get("type", "news")
        
        if content_type == "weather":
            return self._create_weather_image(content)
        elif content_type == "rain_alert":
            return self._create_rain_image(content)
        elif content_type == "traffic":
            return self._create_traffic_image(content)
        elif content_type == "metro":
            return self._create_metro_image(content)
        elif content_type == "poll":
            return self._create_poll_image(content)
        elif content_type == "meme":
            return self._create_meme_image(content)
        else:
            return self._create_news_image(content)
    
    def _create_news_image(self, content: Dict) -> str:
        """Create news post image"""
        image = Image.new('RGB', (self.width, self.height), color=(10, 10, 30))
        draw = ImageDraw.Draw(image)
        
        # Gradient background
        for i in range(self.height):
            color = (int(10 + 40*i/self.height), int(10 + 30*i/self.height), int(30 + 50*i/self.height))
            draw.rectangle([(0, i), (self.width, i+1)], fill=color)
        
        title = content.get("title", "Breaking News")[:60]
        self._draw_text(draw, title, self.height//2, color=(255, 255, 100), size=50)
        self._draw_text(draw, "📰 NEWS", 150, color=(100, 200, 255), size=60)
        
        filepath = self._save_image(image, "news")
        return filepath
    
    def _create_weather_image(self, content: Dict) -> str:
        """Create weather image"""
        image = Image.new('RGB', (self.width, self.height), color=(135, 206, 250))
        draw = ImageDraw.Draw(image)
        
        temp = content.get("temp", 28)
        condition = content.get("condition", "Clear")
        
        # Weather-based colors
        colors = {
            "Clear": (255, 200, 0),
            "Clouds": (150, 150, 150),
            "Rain": (70, 130, 180),
            "Thunderstorm": (50, 50, 100)
        }
        
        bg_color = colors.get(condition, (135, 206, 250))
        
        # Gradient
        for i in range(self.height):
            ratio = i / self.height
            r = int(bg_color[0] * (1-ratio) + 200*ratio)
            g = int(bg_color[1] * (1-ratio) + 150*ratio)
            b = int(bg_color[2] * (1-ratio) + 100*ratio)
            draw.rectangle([(0, i), (self.width, i+1)], fill=(r, g, b))
        
        # Large temperature
        self._draw_text(draw, f"{temp}°C", self.height//2-200, color=(255, 255, 255), size=150)
        
        # Condition
        emoji_map = {"Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Thunderstorm": "⛈️"}
        emoji = emoji_map.get(condition, "🌡️")
        self._draw_text(draw, f"{condition} {emoji}", self.height//2+100, color=(255, 255, 255), size=60)
        
        self._draw_text(draw, "BANGALORE WEATHER", 100, color=(255, 255, 255), size=50)
        
        filepath = self._save_image(image, "weather")
        return filepath
    
    def _create_rain_image(self, content: Dict) -> str:
        """Create rain alert image"""
        image = Image.new('RGB', (self.width, self.height), color=(100, 100, 150))
        draw = ImageDraw.Draw(image)
        
        # Rainy gradient
        for i in range(self.height):
            color = (int(50 + 100*i/self.height), int(100 + 50*i/self.height), int(150 - 50*i/self.height))
            draw.rectangle([(0, i), (self.width, i+1)], fill=color)
        
        # Add rain drops pattern
        import random
        for _ in range(100):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.line([(x, y), (x-5, y+15)], fill=(200, 200, 255), width=2)
        
        will_rain = content.get("will_rain", False)
        if will_rain:
            self._draw_text(draw, "☔ RAIN ALERT ⚠️", 150, color=(255, 100, 100), size=70)
            self._draw_text(draw, "Umbrella Time!", self.height//2+200, color=(255, 255, 255), size=60)
        else:
            self._draw_text(draw, "☀️ CLEAR SKIES", 150, color=(255, 255, 100), size=70)
            self._draw_text(draw, "Perfect Day!", self.height//2+200, color=(255, 255, 255), size=60)
        
        filepath = self._save_image(image, "rain")
        return filepath
    
    def _create_traffic_image(self, content: Dict) -> str:
        """Create traffic image"""
        image = Image.new('RGB', (self.width, self.height), color=(200, 100, 50))
        draw = ImageDraw.Draw(image)
        
        # Gradient
        for i in range(self.height):
            color = (int(200 - 50*i/self.height), int(100 + 30*i/self.height), int(50 + 20*i/self.height))
            draw.rectangle([(0, i), (self.width, i+1)], fill=color)
        
        area = content.get("area", "Bangalore")
        status = content.get("status", "Heavy")
        
        self._draw_text(draw, "🚗 TRAFFIC UPDATE", 100, color=(255, 200, 100), size=60)
        self._draw_text(draw, f"{area}", self.height//2-100, color=(255, 255, 255), size=80)
        self._draw_text(draw, f"{status} Traffic", self.height//2+100, color=(255, 100, 100), size=70)
        
        filepath = self._save_image(image, "traffic")
        return filepath
    
    def _create_metro_image(self, content: Dict) -> str:
        """Create metro image"""
        image = Image.new('RGB', (self.width, self.height), color=(50, 100, 200))
        draw = ImageDraw.Draw(image)
        
        # Gradient
        for i in range(self.height):
            color = (int(50 + 50*i/self.height), int(100 + 50*i/self.height), int(200 - 100*i/self.height))
            draw.rectangle([(0, i), (self.width, i+1)], fill=color)
        
        line = content.get("line", "Metro")
        status = content.get("status", "On Time")
        
        self._draw_text(draw, "🚆 METRO UPDATE", 100, color=(255, 255, 100), size=60)
        self._draw_text(draw, line, self.height//2-100, color=(255, 255, 255), size=80)
        
        status_color = (100, 255, 100) if status == "On Time" else (255, 200, 100)
        self._draw_text(draw, f"✓ {status}", self.height//2+100, color=status_color, size=70)
        
        filepath = self._save_image(image, "metro")
        return filepath
    
    def _create_poll_image(self, content: Dict) -> str:
        """Create poll image"""
        image = Image.new('RGB', (self.width, self.height), color=(100, 50, 150))
        draw = ImageDraw.Draw(image)
        
        # Gradient
        for i in range(self.height):
            color = (int(100 + 50*i/self.height), int(50 + 100*i/self.height), int(150 - 50*i/self.height))
            draw.rectangle([(0, i), (self.width, i+1)], fill=color)
        
        question = content.get("question", "Your Opinion?")[:40]
        
        self._draw_text(draw, "🗳️ POLL", 100, color=(255, 200, 255), size=80)
        self._draw_text(draw, question, self.height//2, color=(255, 255, 255), size=60)
        self._draw_text(draw, "A · B · C", self.height//2+300, color=(200, 255, 200), size=80)
        
        filepath = self._save_image(image, "poll")
        return filepath
    
    def _create_meme_image(self, content: Dict) -> str:
        """Create meme image"""
        image = Image.new('RGB', (self.width, self.height), color=(50, 50, 100))
        draw = ImageDraw.Draw(image)
        
        # Meme-style gradient
        for i in range(self.height):
            color = (random.randint(20, 100), random.randint(20, 100), random.randint(50, 150))
            draw.rectangle([(0, i), (self.width, i+1)], fill=color)
        
        caption = content.get("caption", "Bangalore Vibes")[:35]
        description = content.get("description", "")[:50]
        
        self._draw_text(draw, "😂", 100, color=(255, 255, 255), size=120)
        self._draw_text(draw, caption, self.height//2-100, color=(255, 255, 100), size=60)
        self._draw_text(draw, description[:30], self.height//2+150, color=(255, 255, 255), size=40)
        
        filepath = self._save_image(image, "meme")
        return filepath
    
    def _draw_text(self, draw, text: str, y_pos: int, color=(255, 255, 255), size=50):
        """Helper to draw centered text"""
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x_pos = (self.width - text_width) // 2
        
        draw.text((x_pos, y_pos), text, fill=color, font=font)
    
    def _save_image(self, image: Image, img_type: str) -> str:
        """Save image to file"""
        import time
        filename = f"{img_type}_{int(time.time())}.png"
        filepath = os.path.join(self.output_dir, filename)
        image.save(filepath)
        print(f"✅ Image created: {filepath}")
        return filepath
