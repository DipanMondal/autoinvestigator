import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.risk_reporter import RiskReporterAgent
from agents.pro_risk_analyst import ProRiskAnalystAgent
class Orchestrator:
    """
    The main orchestrator that manages the professional investigation process.
    """
    def __init__(self):
        # Initialize the new ProRiskAnalystAgent
        self.analyst = ProRiskAnalystAgent()
        print("Orchestrator initialized with Professional Risk Analyst. Ready to begin.")

    def run_investigation(self, company_name, ticker, cik):
        """
        Runs a full professional investigation for a given company.

        Args:
            company_name (str): The name of the company to investigate.
            ticker (str): The stock ticker for the company.
            cik (str): The CIK number for SEC filings lookup.

        Returns:
            str: The final, formatted professional risk report.
        """
        print("\n" + "="*50)
        print(f"  STARTING PROFESSIONAL INVESTIGATION: {company_name.upper()}")
        print("="*50)

        # Call the new agent's run method
        final_report = self.analyst.run(company_name, ticker, cik)
        
        print("\n" + "="*50)
        print(f"  INVESTIGATION COMPLETE: {company_name.upper()}")
        print("="*50)
        
        return final_report