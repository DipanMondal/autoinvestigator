# client/mcp_client.py

from agents.company_profiler import CompanyProfilerAgent
from agents.risk_radar import RiskRadarAgent
from agents.news_watcher import NewsWatcherAgent
from agents.financial_intel import FinancialIntelAgent  # ← Add this import

class MCPClient:
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.profiler = CompanyProfilerAgent(company_name)
        self.risk_analyzer = RiskRadarAgent(company_name)
        self.news_watcher = NewsWatcherAgent(company_name)
        self.financial_intel = FinancialIntelAgent(company_name)  # ← Add this line

    def run_pipeline(self):
        print("[MCPClient] Running full pipeline...")
        self.profiler.run()
        self.risk_analyzer.run()
        self.news_watcher.run()
        self.financial_intel.run()  # ← Add this line

    def generate_report(self) -> str:
        return (
            "=== COMPANY PROFILE ===\n" + self.profiler.profile_summary + "\n\n" +
            "=== RISK RADAR ===\n" + self.risk_analyzer.risk_summary + "\n\n" +
            "=== NEWS WATCH ===\n" + self.news_watcher.news_summary + "\n\n" +
            "=== FINANCIAL INTELLIGENCE ===\n" + self.financial_intel.financial_summary + "\n"
        )
