# client/agents/company_profiler.py

from server.tools.web_search import WebSearchTool
from .gemini import GeminiAgent
import json

class CompanyProfilerAgent:
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.web_search_tool = WebSearchTool()
        self.search_results = ""
        self.profile_summary = ""

        # Load the gemini summarization model
        self.summarizer = GeminiAgent()

    def gather_information(self):
        query = f"Detail Company profile of {self.company_name} company profile site:investopedia.com OR site:crunchbase.com OR site:forbes.com OR site:finance.yahoo.com OR site:sec.gov"
        self.search_results = self.web_search_tool.run(query)

    def summarize(self):
        print(f"[CompanyProfilerAgent] Summarizing data for {self.company_name}")
        input_prompt = f"""
You are a corporate intelligence analyst. Based on the following information from the web, generate a concise profile of the company "{self.company_name}". Include sector, founders, year founded, key products, market presence, and any notable events.

Information:
{self.search_results}

Show the result in this format(If any information is not available just replace it with 'unknown'):
{{
    "Company Name : <full comapany name (e.g. Apple->Apple Inc. , Amazon->Amazon.com, Inc.)>,
    "Ticker" : <ticker>,
    "cik" : <cik>,
    "Sector" : <summary>,
    "Founders" : <summary>,
    "Key Products" : <summary comma separated>,
    "Notable Events" : <summary comma separated>,
    "Financials" : {{<summary with key value pair>}}
}}
"""

        summary = self.summarizer.execute(input_prompt)
        self.profile_summary = summary

    def run(self):
        self.gather_information()
        self.summarize()
        return self.profile_summary
        
    def format(self):
        try:
            clean_json = self.profile_summary.strip("`").split("\n", 1)[-1].rsplit("\n", 1)[0]
            data = json.loads(clean_json)
            return data
        except Exception as e:
            return None
