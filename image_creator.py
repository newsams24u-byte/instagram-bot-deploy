from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple

class ImageCreator:
    def __init__(self, width: int = 1080, height: int = 1350):
        self.width = width
        self.height = height
        self.output_dir = "instagram_agent/posts"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_post_image(self, title: str, subtitle: str = "", filename: str = None) -> str:
        """Create an Instagram-ready image with title and subtitle"""
        
        # Create image with gradient-like background
        image = Image.new('RGB', (self.width, self.height), color=(20, 20, 40))
        draw = ImageDraw.Draw(image)
        
        # Add gradient effect (simulate with colored rectangles)
        for i in range(self.height):
            color = (
                int(20 + (100 * i / self.height)),
                int(20 + (50 * i / self.height)),
                int(40 + (80 * i / self.height))
            )
            draw.rectangle([(0, i), (self.width, i+1)], fill=color)
        
        # Add semi-transparent overlay
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 100))
        image.paste(overlay, (0, 0), overlay)
        
        try:
            # Try to use system font, fallback to default
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Add title
        title_lines = self._wrap_text(title, 20)
        y_position = self.height // 3
        
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x_position = (self.width - text_width) // 2
            
            draw.text((x_position, y_position), line, fill=(255, 255, 255), font=title_font)
            y_position += 80
        
        # Add subtitle if provided
        if subtitle:
            subtitle_lines = self._wrap_text(subtitle, 30)
            y_position = self.height - 300
            
            for line in subtitle_lines:
                bbox = draw.textbbox((0, 0), line, font=subtitle_font)
                text_width = bbox[2] - bbox[0]
                x_position = (self.width - text_width) // 2
                
                draw.text((x_position, y_position), line, fill=(100, 200, 255), font=subtitle_font)
                y_position += 60
        
        # Add decorative elements
        self._add_decorations(draw)
        
        # Save image
        if not filename:
            import time
            filename = f"post_{int(time.time())}.png"
        
        filepath = os.path.join(self.output_dir, filename)
        image.save(filepath)
        print(f"✅ Image created: {filepath}")
        
        return filepath
    
    def _wrap_text(self, text: str, width: int) -> list:
        """Wrap text to fit width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= width:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
    
    def _add_decorations(self, draw):
        """Add decorative elements to image"""
        # Add top line
        draw.rectangle([(50, 100), (self.width - 50, 110)], fill=(100, 200, 255))
        
        # Add bottom line
        draw.rectangle([(50, self.height - 110), (self.width - 50, self.height - 100)], fill=(100, 200, 255))
