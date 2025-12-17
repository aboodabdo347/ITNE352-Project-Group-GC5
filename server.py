"""" Server Application Done By Abdulrahaman Abdo - GC5"""
import json
import requests
import os # for accessing environment variables
from dotenv import load_dotenv # for loading environment variables that contain the API key
from datetime import datetime  # for logging timestamps

# Load environment variables
load_dotenv()

# Configuration Constants
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345
GROUP_IDENTIFIER = "GC5"
NEWS_API_BASE = "https://newsapi.org/v2/"
MAX_RESULTS = 15
BUFFER_SIZE = 4096

# Validation Sets
VALID_COUNTRIES = {"au", "ca", "jp", "ae", "sa", "kr", "us", "ma"}
VALID_LANGUAGES = {"ar", "en"}
VALID_CATEGORIES = {"business", "general", "health", "science", "sports", "technology"}


class NewsDataFetcher:
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = NEWS_API_BASE
    
    def get_headlines(self, query_params):
        endpoint = f"{self.base_url}top-headlines"
        return self._execute_request(endpoint, query_params)
    
    def get_news_sources(self, query_params):
        endpoint = f"{self.base_url}sources"
        return self._execute_request(endpoint, query_params)
    
    def _execute_request(self, endpoint, query_params):
        request_params = dict(query_params)
        request_params["apiKey"] = self.api_key
        
        try:
            api_response = requests.get(endpoint, params=request_params, timeout=10)
            api_response.raise_for_status()
            return api_response.json()
        except requests.RequestException as error:
            raise ConnectionError(f"API request failed: {error}")
        
class ParameterValidator:   # Validates client request parameters against allowed values

    @staticmethod  # makes the function callable on the class without receiving a self parameter
    def validate_headline_params(params): # Validate parameters for headline requests
        validated = {}
        if "q" in params:
            keyword = params["q"].strip()
            if not keyword:
                return None, "Search keyword cannot be empty"
            validated["q"] = keyword
        
        # Validate category
        if "category" in params:
            category = params["category"]
            if category not in VALID_CATEGORIES:
                return None, f"Invalid category. Choose from: {', '.join(sorted(VALID_CATEGORIES))}"
            validated["category"] = category
        
        # Validate country code
        if "country" in params:
            country = params["country"]
            if country not in VALID_COUNTRIES:
                return None, f"Invalid country code. Choose from: {', '.join(sorted(VALID_COUNTRIES))}"
            validated["country"] = country
        
        # Set default country for general queries
        if not any(key in validated for key in ["country", "q", "category"]):
            validated["country"] = "us"
        
        return validated, None
    
    @staticmethod
    def validate_source_params(params): # Validate parameters for source requests
        validated = {}
        
        # Validate category
        if "category" in params:
            category = params["category"]
            if category not in VALID_CATEGORIES:
                return None, f"Invalid category. Choose from: {', '.join(sorted(VALID_CATEGORIES))}"
            validated["category"] = category
        
        # Validate country code
        if "country" in params:
            country = params["country"]
            if country not in VALID_COUNTRIES:
                return None, f"Invalid country code. Choose from: {', '.join(sorted(VALID_COUNTRIES))}"
            validated["country"] = country
        
        # Validate language
        if "language" in params:
            language = params["language"]
            if language not in VALID_LANGUAGES:
                return None, f"Invalid language. Choose from: {', '.join(sorted(VALID_LANGUAGES))}"
            validated["language"] = language
        
        return validated, None
