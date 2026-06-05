"""
WSGI entry point for production deployment
Use this for Render, Heroku, PythonAnywhere, etc.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from web_app import app

if __name__ == "__main__":
    app.run()
