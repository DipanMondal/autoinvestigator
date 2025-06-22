# client/agents/financial_intel.py

from server.tools.financial_data import FinancialDataTool
from server.tools.sec_filings import SECFilingsTool
from server.tools.web_search import WebSearchTool
from .gemini import GeminiAgent
from duckduckgo_search import DDGS
import json

class FinancialIntelAgent:
    """
    Analyzes a company's financial health using Yahoo Finance and SEC filings.
    Generates a summary using Gemini AI.
    """

    def __init__(self,company_name:str, ticker: str, cik: str):
        """
            initialises The FinancialIntelAgent
            
            Args:
            company_name: string, name of the company
            ticker : string , ticker of the company
            cik : string , cik id of the company
        """
        self.company_name = company_name
        self.ticker = ticker
        self.cik = cik
        self.finance_tool = FinancialDataTool()
        self.sec_tool = SECFilingsTool()
        self.summarizer = GeminiAgent()
        self.summary = ""
        if not self.cik:
            self.cik = self.get_cik()
        print(self.cik)
    
    def get_cik(self):
        """ Search the web to get the cik number """
        searcher = WebSearchTool()
        query = f"CIK number for {self.company_name} site:sec.gov"
        
        context = WebSearchTool().run(query)
        
        prompt = f"""
        You are a financial advencer. Here is the context of a company:
        {context}
        
        Give me onle the cik number in this format:
        {{"cik":<cik number>}}
        If available in the context, otherwise you can take help from your memory or 'None'"""
        res = self.summarizer.execute(prompt)
        print(res)
        try:
            clean_json = res.strip("`").split("\n", 1)[-1].rsplit("\n", 1)[0]
            data = json.loads(clean_json)
            return data["cik"]
        except Exception as e:
            print(e)
            return None

    def collect_data(self):
        print("[FinancialIntelAgent] Collecting financial data")
        finance_info = self.finance_tool.run(self.ticker)
        sec_info = self.sec_tool.run(self.cik)

        return finance_info, sec_info

    def summarize(self, finance_info: str, sec_info: str):
        prompt = f"""
You are a financial analyst. Based on the following information from Yahoo Finance and SEC filings, 
generate a financial intelligence report for the company {self.ticker}. Include valuation, performance, any red flags or highlights.

YAHOO FINANCE:
{finance_info}

SEC FILINGS:
{sec_info}
"""
        trimmed = prompt[:4000]
        self.summary = self.summarizer.execute(trimmed)

    def run(self):
        finance_info, sec_info = self.collect_data()
        self.summarize(finance_info, sec_info)
        return self.summary
