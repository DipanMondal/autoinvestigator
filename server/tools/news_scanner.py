# server/tools/news_scanner.py

from duckduckgo_search import DDGS
from shared.config import REGION,SAFE_SEARCH, TIME_LIMIT, MAX_RESULTS
from server.tools.web_search import WebSearchTool

class NewsScannerTool:
    """
    Scans recent news articles related to lawsuits, fraud, or other risks for a given company.
    """
    def __init__(self):
        self.web_search = WebSearchTool()
    def run(self, company_name: str) -> str:
        print(f"[NewsScannerTool] Searching risk-related news for {company_name}")
        query = f"{company_name} lawsuit fraud OR scandal OR investigation OR controversy"
        results = self.web_search.run(query=query);
        return results
