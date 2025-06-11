# client/agents/company_profiler.py

from server.tools.web_search import WebSearchTool
from shared.gemini import GeminiAgent

class CompanyProfilerAgent:
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.web_search_tool = WebSearchTool()
        self.search_results = ""
        self.profile_summary = ""

        # Load the gemini summarization model
        self.summarizer = GeminiAgent()

    def gather_information(self):
        query = f"{self.company_name} company profile site:investopedia.com OR site:crunchbase.com OR site:forbes.com"
        self.search_results = self.web_search_tool.run(query)

    def summarize(self):
        print(f"[CompanyProfilerAgent] Summarizing data for {self.company_name}")
        input_text = f"""
You are a corporate intelligence analyst. Based on the following information from the web, generate a concise profile of the company "{self.company_name}". Include sector, founders, year founded, key products, market presence, and any notable events.

Information:
{self.search_results}
"""

        # Hugging Face pipeline has input length limits (~1024 tokens)
        trimmed = input_text[:4000]  # Limit input length to avoid overflow
        summary = self.summarizer.execute(trimmed)
        self.profile_summary = summary

    def run(self):
        self.gather_information()
        self.summarize()
        return self.profile_summary
