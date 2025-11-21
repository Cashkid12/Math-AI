"""
Configuration module for Equai AI backend
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    MONGODB_URI = os.getenv('MONGODB_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'equai_db')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))
    
    # Graph settings
    GRAPH_DPI = 100
    GRAPH_FIGSIZE = (10, 6)
    GRAPH_DIR = 'static/graphs'
    
    # Math solver settings
    MAX_STEPS = 50  # Maximum number of solution steps to show