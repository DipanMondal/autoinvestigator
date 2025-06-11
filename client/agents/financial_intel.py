# client/agents/financial_intel.py

from server.tools.financial_data import FinancialDataTool
from server.tools.sec_filings import SECFilingsTool
from .gemini import GeminiAgent

class FinancialIntelAgent:
    """
    Analyzes a company's financial health using Yahoo Finance and SEC filings.
    Generates a summary using Gemini AI.
    """

    def __init__(self, ticker: str, cik: str):
        self.ticker = ticker
        self.cik = cik
        self.finance_tool = FinancialDataTool()
        self.sec_tool = SECFilingsTool()
        self.summarizer = GeminiAgent()
        self.summary = ""

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
