import os
import requests
from typing import Optional

class InstagramPoster:
    def __init__(self):
        # Option 1: Using Instagram Graph API (recommended for business accounts)
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.business_account_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
        self.graph_api_url = "https://graph.instagram.com/v18.0"
        
        # Option 2: Using instagrapi (for personal accounts)
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.use_graph_api = bool(self.access_token and self.business_account_id)
    
    def post_to_instagram(self, image_path: str, caption: str) -> bool:
        """Post image to Instagram"""
        if self.use_graph_api:
            return self._post_via_graph_api(image_path, caption)
        else:
            return self._post_via_instagrapi(image_path, caption)
    
    def _post_via_graph_api(self, image_path: str, caption: str) -> bool:
        """Post using Instagram Graph API (Business Account)"""
        try:
            # Step 1: Upload image and get media ID
            with open(image_path, 'rb') as f:
                files = {'image': f}
                params = {
                    'user_id': self.business_account_id,
                    'access_token': self.access_token
                }
                
                response = requests.post(
                    f"{self.graph_api_url}/{self.business_account_id}/media",
                    files=files,
                    params=params
                )
            
            if response.status_code != 200:
                print(f"❌ Upload failed: {response.text}")
                return False
            
            media_id = response.json().get('id')
            print(f"✅ Media uploaded. ID: {media_id}")
            
            # Step 2: Publish the media
            publish_params = {
                'user_id': self.business_account_id,
                'caption': caption,
                'access_token': self.access_token
            }
            
            publish_response = requests.post(
                f"{self.graph_api_url}/{media_id}/publish",
                params=publish_params
            )
            
            if publish_response.status_code == 200:
                print(f"✅ Posted successfully to Instagram!")
                return True
            else:
                print(f"❌ Publish failed: {publish_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error posting via Graph API: {e}")
            return False
    
    def _post_via_instagrapi(self, image_path: str, caption: str) -> bool:
        """Post using instagrapi (Personal Account)"""
        try:
            from instagrapi import Client
            
            cl = Client()
            cl.login(self.username, self.password)
            
            media = cl.photo_upload(image_path, caption=caption)
            print(f"✅ Posted successfully! Media ID: {media.id}")
            return True
            
        except Exception as e:
            print(f"❌ Error posting via instagrapi: {e}")
            return False
    
    def is_configured(self) -> bool:
        """Check if Instagram credentials are configured"""
        return (self.access_token and self.business_account_id) or (self.username and self.password)
