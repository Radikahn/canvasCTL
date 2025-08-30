"""Configuration management for Canvas Calendar application."""

import os
from dotenv import load_dotenv
from typing import List

class Config:
    """Configuration class for Canvas API and application settings."""
    
    def __init__(self):
        load_dotenv()
        self._validate_env_vars()
    
    @property
    def api_url(self) -> str:
        return os.getenv("API_URL")
    
    @property
    def api_key(self) -> str:
        return os.getenv("API_KEY")
    
    @property
    def course_list(self) -> List[str]:
        return os.getenv("COURSE_LIST", "").split(",")
    
    def _validate_env_vars(self):
        """Validate that required environment variables are set."""
        required_vars = ["API_URL", "API_KEY", "COURSE_LIST"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")