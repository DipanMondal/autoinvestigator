from googleapiclient.discovery import build
from shared.config import GOOGL_SEARCH_KEY,CSE,SERP_KEY
import os
import time
import requests

class WebSearchTool:
    def __init__(self):
        self.ggl_api_key = os.getenv(GOOGL_SEARCH_KEY)
        self.serp_api_key = os.getenv(SERP_KEY)
        self.cse_id = os.getenv(CSE)
        self.service = build("customsearch", "v1", developerKey=self.ggl_api_key)

    def __google(self, query: str,num_results=5): # No change to this method's logic
        print(f"[WebSearchTool] Searching Google for: {query}")
        extracted = []
        
        max_retries = 5
        base_delay = 1
        for attempt in range(max_retries):
            try:
                results = self.service.cse().list(
                    q=query,
                    cx=self.cse_id,
                    num=num_results
                ).execute()
                
                for result in results.get('items',[]):
                    # --- CHANGE 1: Append a dictionary instead of a formatted string ---
                    extracted.append({
                        "Title": result.get('title'),
                        "Body": result.get('snippet'),
                        "Source": result.get('link')
                    })
            except Exception as e:
                time.sleep(base_delay)
                print(f"An error occurred: {e}")
        return extracted
    
    def __serp(self,query:str,num_results:int=5): # No change to this method's logic
        print(f"[WebSearchTool] Searching SERP for: {query}")
        params = {
            "q": query,
            "api_key": self.serp_api_key,
            "engine": "google",
            "num": num_results
        }

        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json()

        extracted = []
        for result in results.get("organic_results", []):
            # --- CHANGE 2: Append a dictionary instead of a formatted string ---
            extracted.append({
                "Title": result.get("title"),
                "Body": result.get("snippet"),
                "Source": result.get("link")
            })
        return extracted
        
    def run(self,query:str, num_results:int=5):
        """
        This tool searches the Web and returns structured results.
        """
        extracted = [] # Initialize as an empty list
        try:
            extracted = self.__google(query,num_results)
            if len(extracted)==0:
                extracted = self.__serp(query,num_results)
        except Exception as e:
            print(f"Error occured while searching the web: {e}")
        
        # --- CHANGE 3: Return the raw list of dictionaries ---
        return extracted if extracted else []