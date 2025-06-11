# server/tools/web_search.py

import os
import requests

class WebSearchTool:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")
        if not self.api_key:
            raise EnvironmentError("Set SERPAPI_KEY in environment")

    def run(self, query: str) -> str:
        print(f"[WebSearchTool] Searching SerpAPI for: {query}")
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google",
            "num": 5
        }

        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json()

        extracted = []
        for result in results.get("organic_results", []):
            snippet = result.get("snippet")
            link = result.get("link")
            if snippet:
                extracted.append(f"{snippet}\n(Source: {link})")

        return "\n\n".join(extracted) if extracted else "No relevant search results found."
