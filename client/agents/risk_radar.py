# client/agents/risk_radar.py

from server.tools.news_scanner import NewsScannerTool
from .gemini import GeminiAgent

class RiskRadarAgent:
    """
    Analyzes recent news to detect red flags like lawsuits, scandals, fraud, and investigations.
    """

    def __init__(self, company_name: str):
        self.company_name = company_name
        self.news_tool = NewsScannerTool()
        self.summarizer = GeminiAgent()
        self.risk_summary = ""

    def gather_news(self):
        print(f"[RiskRadarAgent] Gathering risk news for {self.company_name}")
        return self.news_tool.run(self.company_name)

    def summarize_risks(self, news: str):
        prompt = f"""
You are a corporate risk analyst. Based on the following news articles, write a concise risk report for "{self.company_name}".
Identify any lawsuits, frauds, controversies, or reputational risks.

NEWS:
{news}
"""
        trimmed = prompt[:4000]
        self.risk_summary = self.summarizer.execute(trimmed)

    def run(self):
        news_data = self.gather_news()
        self.summarize_risks(news_data)
        return self.risk_summary
