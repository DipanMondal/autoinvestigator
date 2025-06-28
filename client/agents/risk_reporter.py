import sys
import os
import json

# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_client import MCPClient
from agents.company_profiler import CompanyProfilerAgent
from agents.news_watcher import NewsWatcherAgent

class RiskReporterAgent:
    """
    An agent that orchestrates data gathering and uses an AI model
    to generate a final risk report.
    """
    def __init__(self):
        self.client = MCPClient()
        self.profiler = CompanyProfilerAgent()
        self.news_watcher = NewsWatcherAgent()
        print("Risk Reporter Agent initialized.")

    def run(self, company_name, ticker):
        """
        Executes the full investigation and reporting task.
        
        Args:
            company_name (str): The name of the company.
            ticker (str): The stock ticker of the company.
            
        Returns:
            str: The final generated risk report.
        """
        print(f"\n--- Starting Full Investigation for {company_name} ---")

        # 1. Gather data using other agents
        print("\nStep 1: Gathering company profile and financial data...")
        profile_data = self.profiler.run(company_name, ticker)
        
        print("\nStep 2: Scanning for recent news...")
        news_articles = self.news_watcher.run(company_name)

        # 2. Compile the collected data into a single context
        full_context = {
            "profile": profile_data,
            "news": news_articles
        }

        print("\nStep 3: Analyzing data and generating report...")
        
        # 3. Create a prompt for the Gemini model
        prompt = f"""
        You are a professional corporate risk analyst. Based on the following data, please generate a concise risk report for the company '{company_name}'.
        The report should include:
        1. A brief summary of the company based on its web profile.
        2. A summary of key financial data.
        3. An analysis of recent news, highlighting any potential risks (e.g., lawsuits, fraud, scandals, investigations).
        4. A final conclusion on the company's overall risk level (Low, Medium, High).

        Here is the data:
        {json.dumps(full_context, indent=2)}
        """

        # 4. Call the Gemini tool on the server
        gemini_params = {"query": prompt}
        report_response = self.client.execute_tool("tools/gemini", gemini_params)

        final_report = "Could not generate report."
        if report_response and "results" in report_response:
            try:
                # Extract the generated text from the response
                final_report = report_response["results"][0].get("results", [])[0]
            except (IndexError, KeyError) as e:
                print(f"Error parsing Gemini response: {e}")

        print("\n--- Investigation Complete ---")
        return final_report


if __name__ == '__main__':
    # Make sure the server is running in another terminal!
    
    reporter_agent = RiskReporterAgent()
    
    # Generate a report for a company (e.g., 'Tesla')
    final_report = reporter_agent.run(company_name="Tesla", ticker="TSLA")

    # Print the final report
    print("\n\n--- FINAL RISK REPORT ---")
    print(final_report)
    print("-------------------------")