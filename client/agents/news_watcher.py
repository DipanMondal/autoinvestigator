# client/agents/news_watcher.py

from transformers import pipeline
from server.tools.news_aggregator import NewsAggregatorTool
from .gemini import GeminiAgent

class NewsWatcherAgent:
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.news_tool = NewsAggregatorTool()
        self.raw_news = ""
        self.summary = ""
        self.summarizer = GeminiAgent()

    def fetch_news(self):
        self.raw_news = self.news_tool.run(self.company_name)

    def summarize_news(self):
        print(f"[NewsWatcherAgent] Summarizing news for {self.company_name}")
        input_text = f"""
As a corporate risk analyst, review the latest news for the company "{self.company_name}". 
Summarize major updates, controversies, financial performance, regulatory changes, or executive moves.

News:
{self.raw_news}
"""
        trimmed = input_text[:4000]
        summary = self.summarizer.execute(trimmed)
        self.summary = summary

    def run(self):
        self.fetch_news()
        self.summarize_news()
        return self.summary
