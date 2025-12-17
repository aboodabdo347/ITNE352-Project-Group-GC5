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
        """Fetch news sources based on provided parameters"""
        endpoint = f"{self.base_url}sources"
        return self._execute_request(endpoint, query_params)
    
    def _execute_request(self, endpoint, query_params):
        """Execute HTTP GET request to API endpoint"""
        request_params = dict(query_params)
        request_params["apiKey"] = self.api_key
        
        try:
            api_response = requests.get(endpoint, params=request_params, timeout=10)
            api_response.raise_for_status()
            return api_response.json()
        except requests.RequestException as error:
            raise ConnectionError(f"API request failed: {error}")
if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("API_KEY not set; module imported without executing fetch.")
    else:
        fetcher = NewsDataFetcher(api_key)
        params = {"country": list(VALID_COUNTRIES)[1], "pageSize": MAX_RESULTS}
        try:
            result = fetcher.get_headlines(params)
            print((VALID_COUNTRIES)[1])
        except ConnectionError as e:
            print(f"Failed to fetch headlines: {e}")