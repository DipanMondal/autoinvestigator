import sys
import os
import json
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_client import MCPClient
from agents.company_profiler import CompanyProfilerAgent
from agents.news_watcher import NewsWatcherAgent

class ProRiskAnalystAgent:
    """
    A professional-grade agent that performs deep analysis using advanced tools
    like sentiment analysis and SEC filing reviews.
    """
    def __init__(self):
        self.client = MCPClient()
        self.profiler = CompanyProfilerAgent()
        self.news_watcher = NewsWatcherAgent()
        print("Professional Risk Analyst Agent initialized.")

    def run(self, company_name, ticker, cik):
        print(f"\n--- Starting Professional Investigation for {company_name} ---")

        # Step 1: Standard data gathering
        print("\n[Step 1/4] Gathering company profile and financial data...")
        profile_data = self.profiler.run(company_name, ticker)

        # Step 2: SEC Filings Analysis
        print(f"\n[Step 2/4] Retrieving and analyzing SEC Filings (CIK: {cik})...")
        sec_filings_summary = "No SEC filings found or CIK not provided."
        if cik:
            sec_response = self.client.execute_tool("tools/sec_filings", {"cik": cik})
            if sec_response and sec_response.get("results"):
                sec_filings_summary = sec_response["results"][0].get("results", [""])[0]

        # Step 3: News Gathering and Sentiment Analysis
        print("\n[Step 3/4] Scanning news and analyzing sentiment...")
        news_articles = self.news_watcher.run(company_name)
        analyzed_news = []
        if news_articles:
            for article in news_articles:
                title = article.get('Title', '')
                sentiment_response = self.client.execute_tool("tools/sentiment", {"text": title})
                sentiment = {"compound": 0.0} # Default neutral
                if sentiment_response and sentiment_response.get("results"):
                    sentiment = sentiment_response["results"][0].get("results", [{}])[0]
                
                analyzed_news.append({
                    "article": article,
                    "sentiment": sentiment
                })

        # Step 4: Final AI-Powered Reporting
        print("\n[Step 4/4] Compiling data and generating final professional report...")
        
        prompt = self._build_professional_prompt(company_name, profile_data, sec_filings_summary, analyzed_news)
        
        gemini_params = {"query": prompt}
        report_response = self.client.execute_tool("tools/gemini", gemini_params)

        final_report = "Could not generate report."
        if report_response and "results" in report_response:
            try:
                final_report = report_response["results"][0].get("results", [""])[0]
            except (IndexError, KeyError) as e:
                print(f"Error parsing Gemini response: {e}")
        
        return final_report

    def _build_professional_prompt(self, company_name, profile, sec_summary, news):
        """Builds the advanced prompt for the Gemini model."""
        
        # Summarize news sentiment
        negative_news = [item for item in news if item['sentiment']['compound'] <= -0.05]
        
        return f"""
        As a senior risk analyst at a top-tier investment firm, create a comprehensive and structured risk assessment report for '{company_name}'.

        **Objective:** To provide a clear, evidence-based evaluation of the company's risk profile for investment purposes.

        **Source Data:**
        1.  **Company Profile & Financials:** {json.dumps(profile, indent=2)}
        2.  **Summary of SEC Filings:** {sec_summary}
        3.  **Recent News with Sentiment Analysis:** {json.dumps(news, indent=2)}

        **Required Report Structure:**

        **1. Executive Summary:**
           - Brief overview of the company.
           - Final risk assessment (Low, Medium, High, Critical).
           - Key driving factors for this assessment.

        **2. Financial Health Analysis:**
           - Summarize key metrics from the provided financial data.
           - Comment on financial stability, profitability, and debt.

        **3. Public Perception & News Analysis:**
           - Summarize the overall sentiment from recent news.
           - Detail the most significant negative news items ({len(negative_news)} found). For each, provide the source and analyze its potential impact. Reference the sentiment score.

        **4. Regulatory and Self-Reported Risks (from SEC Filings):**
           - Analyze the key risks highlighted in the company's own SEC filings.
           - Mention any discrepancies between self-reported risks and risks observed in the news.

        **5. Final Recommendation:**
           - Conclude with a clear risk rating.
           - Provide a concise justification for your recommendation, synthesizing all analyzed points.

        Produce the report in well-formatted Markdown.
        """