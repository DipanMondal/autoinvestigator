# client/main.py


import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.company_profiler import CompanyProfilerAgent
from agents.news_watcher import NewsWatcherAgent
from agents.financial_intel import FinancialIntelAgent
from agents.risk_radar import RiskRadarAgent

if __name__ == "__main__":
    company_name = "Apple"
    
    #print("\n===== COMPANY PROFILE =====")
    #profile_agent = CompanyProfilerAgent(company_name)
    #profile_summary = profile_agent.run()
    #print(profile_summary)

    #print("\n===== LATEST NEWS SUMMARY =====")
    #news_agent = NewsWatcherAgent(company_name)
    #news_summary = news_agent.run()
    #print(news_summary)
    
    #print("\n===== FINANCIAL INTELLIGENCE =====")
    #intel_agent = FinancialIntelAgent(ticker="AAPL", cik="0000320193")
    #intel_summary = intel_agent.run()
    #print(intel_summary)
    
    
    print("\n===== RISK RADAR =====")
    risk_agent = RiskRadarAgent(company_name="Apple")
    risk_report = risk_agent.run()
    print(risk_report)

