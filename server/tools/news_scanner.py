# server/tools/news_scanner.py

from duckduckgo_search import DDGS
from shared.config import REGION,SAFE_SEARCH, TIME_LIMIT, MAX_RESULTS

class NewsScannerTool:
    """
    Scans recent news articles related to lawsuits, fraud, or other risks for a given company.
    """

    def run(self, company_name: str) -> str:
        print(f"[NewsScannerTool] Searching risk-related news for {company_name}")
        query = f"{company_name} lawsuit fraud OR scandal OR investigation OR controversy"
        try:
            results = DDGS().news(
                keywords=query,
                region=REGION,
                safesearch=SAFE_SEARCH,
                timelimit=TIME_LIMIT,
                max_results=MAX_RESULTS
            )
        except Exception:
            return "Unable to perform news search."

        if not results:
            return "No risk-related news found."

        articles = [
            f"Title : {res['title']} - (Sourse){res['url']}\nBody : {res['body']}"
            for res in results
        ]
        return "\n\n".join(articles)
