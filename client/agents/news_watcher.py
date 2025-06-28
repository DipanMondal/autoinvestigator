import sys
import os
import json

# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_client import MCPClient

class NewsWatcherAgent:
    """
    An agent that specializes in scanning for recent news about a company.
    """
    def __init__(self):
        self.client = MCPClient()
        print("News Watcher Agent initialized.")

    def run(self, company_name):
        """
        Executes the news scanning task for a given company.
        
        Args:
            company_name (str): The name of the company to scan for news.
            
        Returns:
            list: A list of news articles found.
        """
        print(f"\n--- Starting news scan for {company_name} ---")
        
        news_articles = []

        # Use the client to call the 'tools/news' endpoint
        news_params = {"name": company_name}
        news_response = self.client.execute_tool("tools/news", news_params)
        
        if news_response and "results" in news_response:
            try:
                # --- FIX ---
                # The server returns a list containing the direct results.
                # We access the first item of the outer list, then the inner results.
                news_articles = news_response["results"][0].get("results", [])[0]
            except (IndexError, KeyError, TypeError) as e:
                print(f"Could not parse news results due to structure issue or empty response: {e}")

        # Ensure we always return a list
        if not isinstance(news_articles, list):
             news_articles = [news_articles] if news_articles else []

        print(f"--- Found {len(news_articles)} news articles ---")
        return news_articles


if __name__ == '__main__':
    # This block demonstrates how to use the agent
    
    # Make sure the server is running in another terminal!
    
    news_agent = NewsWatcherAgent()
    
    # Scan for news about a company (e.g., Microsoft)
    articles = news_agent.run(company_name="Microsoft")

    # Print the final list of articles
    print("\n\n--- FOUND NEWS ARTICLES ---")
    print(json.dumps(articles, indent=2))
    print("--------------------------")