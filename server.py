"""" Server Application Done By Abdulrahaman Abdo - GC5"""
import json
import socket
import threading
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
class ClientConnectionHandler(threading.Thread):
    # Manages individual client connection in separate thread 
    
    def __init__(self, server_instance, client_sock, client_addr):
        super().__init__(daemon=True)
        self.server = server_instance
        self.socket = client_sock
        self.address = client_addr
        self.receive_buffer = b""
        self.username = None
        self.cached_headlines = []
        self.cached_sources = []
    
    def run(self):
        # Main thread execution method 
        try:
            self._setup_connection()
            self._process_client_requests()
        except Exception as error:
            self._log(f"Error handling client: {error}")
        finally:
            self.socket.close()
            if self.username:
                self._log(f"Client {self.username} disconnected")
    
    def _setup_connection(self):
        # Initialize client connection and receive username 
        username_data = self.socket.recv(1024).decode().strip()
        self.username = username_data if username_data else "Guest"
        self._log(f"Client connected: {self.username} from {self.address}")
    
    def _process_client_requests(self):
        # Main request processing loop
        while True:
            request_data = self._receive_message()
            if not request_data:
                break
            
            action_type = request_data.get("action")
            action_params = request_data.get("params", {})
            
            if action_type == "quit":
                self._send_message({"status": "ok", "message": "Connection closed"})
                break
            
            self._log(f"Request from {self.username}: {action_type} with params {action_params}")
            response_data = self._handle_action(action_type, action_params)
            self._send_message(response_data)
    
    def _handle_action(self, action_type, action_params):
        # Route action to appropriate handler 
        try:
            if action_type.startswith("headlines_"):
                return self._process_headline_action(action_type, action_params)
            elif action_type.startswith("sources_"):
                return self._process_source_action(action_type, action_params)
            else:
                return {"status": "error", "message": "Unknown action type"}
        except Exception as error:
            return {"status": "error", "message": str(error)}
    
    def _process_headline_action(self, action_type, action_params):
        # Handle headline-related actions 
        if action_type == "headlines_detail":
            return self._get_headline_detail(action_params)
        
        # Validate parameters
        validated_params, error_msg = ParameterValidator.validate_headline_params(action_params)
        if error_msg:
            return {"status": "error", "message": error_msg}
        
        # Fetch data from API
        api_data = self.server.data_fetcher.get_headlines(validated_params)
        self._save_response_to_file(action_type, api_data)
        
        # Process and cache results
        articles = api_data.get("articles", [])[:MAX_RESULTS]
        self.cached_headlines = articles
        
        # Build response list
        response_items = []
        for idx, article in enumerate(articles, 1):
            response_items.append({
                "index": idx,
                "source": article.get("source", {}).get("name"),
                "author": article.get("author"),
                "title": article.get("title")
            })
        
        return {
            "status": "ok",
            "type": "headlines_list",
            "items": response_items,
            "total": len(articles)
        }
    
    def _get_headline_detail(self, params):
        # Retrieve detailed information for specific headline 
        try:
            index = int(params.get("index", 0))
        except ValueError:
            return {"status": "error", "message": "Invalid index format"}
        
        if index < 1 or index > len(self.cached_headlines):
            return {"status": "error", "message": "Index out of range"}
        
        article = self.cached_headlines[index - 1]
        return {
            "status": "ok",
            "type": "headline_detail",
            "detail": {
                "source": article.get("source", {}).get("name"),
                "author": article.get("author"),
                "title": article.get("title"),
                "url": article.get("url"),
                "description": article.get("description"),
                "publishedAt": article.get("publishedAt")
            }
        }
    
    def _process_source_action(self, action_type, action_params):
        # Handle source-related actions 
        if action_type == "sources_detail":
            return self._get_source_detail(action_params)
        
        # Validate parameters
        validated_params, error_msg = ParameterValidator.validate_source_params(action_params)
        if error_msg:
            return {"status": "error", "message": error_msg}
        
        # Fetch data from API
        api_data = self.server.data_fetcher.get_news_sources(validated_params)
        self._save_response_to_file(action_type, api_data)
        
        # Process and cache results
        sources = api_data.get("sources", [])[:MAX_RESULTS]
        self.cached_sources = sources
        
        # Build response list
        response_items = []
        for idx, source in enumerate(sources, 1):
            response_items.append({
                "index": idx,
                "name": source.get("name")
            })
        
        return {
            "status": "ok",
            "type": "sources_list",
            "items": response_items,
            "total": len(sources)
        }
    
    def _get_source_detail(self, params):
        try:
            index = int(params.get("index", 0))
        except ValueError:
            return {"status": "error", "message": "Invalid index format"}
        
        if index < 1 or index > len(self.cached_sources):
            return {"status": "error", "message": "Index out of range"}
        
        source = self.cached_sources[index - 1]
        return {
            "status": "ok",
            "type": "source_detail",
            "detail": {
                "name": source.get("name"),
                "country": source.get("country"),
                "description": source.get("description"),
                "url": source.get("url"),
                "category": source.get("category"),
                "language": source.get("language")
            }
        }
    
    def _save_response_to_file(self, action_name, data):
        sanitized_action = action_name.replace(" ", "_")
        filename = f"{self.username}_{sanitized_action}_{GROUP_IDENTIFIER}.json"
        
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    
    def _receive_message(self):
        while b"\n" not in self.receive_buffer:
            chunk = self.socket.recv(BUFFER_SIZE)
            if not chunk:
                return None
            self.receive_buffer += chunk
        
        message_data, self.receive_buffer = self.receive_buffer.split(b"\n", 1)
        try:
            return json.loads(message_data.decode())
        except json.JSONDecodeError:
            return None
    
    def _send_message(self, data):
        message = json.dumps(data) + "\n"
        self.socket.sendall(message.encode())
    
    def _log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        print(f"[{timestamp}] {message}")
class NewsServerApplication:
    # Main server application managing client connections 
    
    def __init__(self, host, port, api_key):
        self.host = host
        self.port = port
        self.data_fetcher = NewsDataFetcher(api_key)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def start(self):
        # Start server and accept client connections 
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(3)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Server started on {self.host}:{self.port}")
        print(f"[{timestamp}] Waiting for client connections...")
        
        try:
            while True:
                client_sock, client_addr = self.server_socket.accept()
                handler = ClientConnectionHandler(self, client_sock, client_addr)
                handler.start()
        except KeyboardInterrupt:
            print("\n[Server] Shutting down...")
        finally:
            self.server_socket.close()


def main():
    # Application entry point 
    # Load API key from environment
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        print("Error: API_KEY not found in environment variables")
        print("Please create a .env file with: API_KEY=your_api_key_here")
        return
    
    server = NewsServerApplication(SERVER_HOST, SERVER_PORT, api_key)
    server.start()


if __name__ == "__main__":
    main()