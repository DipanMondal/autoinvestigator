import sys
import os
import json

# This is a common way to handle imports in a multi-directory project.
# It adds the project's root directory to the Python path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_client import MCPClient

class CompanyProfilerAgent:
    """
    An agent responsible for gathering and profiling a company using available tools.
    """
    def __init__(self):
        self.client = MCPClient()
        print("Company Profiler Agent initialized.")

    def run(self, company_name, ticker, cik=None):
        """
        Executes the profiling task for a given company.
        
        Args:
            company_name (str): The name of the company to profile.
            ticker (str): The stock ticker of the company.
            cik (str, optional): The CIK number for financial data. Defaults to None.
        
        Returns:
            dict: A dictionary containing the compiled profile information.
        """
        print(f"\n--- Starting profiling for {company_name} ---")
        
        profile = {
            "company_name": company_name,
            "ticker": ticker,
            "web_search_results": None,
            "financial_data": None
        }

        # 1. Perform a web search for general information
        print(f"Executing web search for '{company_name}'...")
        search_params = {"query": f"latest news and overview of {company_name}"}
        search_response = self.client.execute_tool("tools/websearch", search_params)
        
        if search_response and "results" in search_response:
            # Assuming the first result is the most relevant
            profile["web_search_results"] = search_response["results"][0].get("results", [])

        # 2. Fetch financial data for the company
        print(f"Executing financial data search for ticker '{ticker}'...")
        financial_params = {"ticker": ticker, "cik": cik}
        financial_response = self.client.execute_tool("tools/financial_descriptor", financial_params)

        if financial_response and "results" in financial_response:
            profile["financial_data"] = financial_response["results"][0].get("results", [])

        print("--- Profiling complete ---")
        return profile


if __name__ == '__main__':
    # This block demonstrates how to use the agent
    
    # Make sure the server is running in another terminal before executing this!
    
    profiler_agent = CompanyProfilerAgent()
    
    # Profile a company (e.g., Apple Inc.)
    company_profile = profiler_agent.run(company_name="Apple Inc.", ticker="AAPL")

    # Print the final compiled profile
    print("\n\n--- COMPILED COMPANY PROFILE ---")
    print(json.dumps(company_profile, indent=2))
    print("---------------------------------")