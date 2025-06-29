from orchestrator import Orchestrator
import textwrap

def main():
    """
    The main function for the professional command-line user interface.
    """
    print("="*60)
    print("      Welcome to the Professional AutoInvestigator System")
    print("="*60)

    # Initialize the main orchestrator
    orchestrator = Orchestrator()

    try:
        while True:
            print("\nPlease provide the details of the company to investigate.")
            company_name = input("Enter the company name (e.g., Tesla): ")
            ticker = input(f"Enter the stock ticker for {company_name} (e.g., TSLA): ")
            # Add a prompt for the CIK number
            cik = input(f"Enter the CIK for {company_name} (e.g., 1318605, leave blank if none): ")

            if not company_name or not ticker:
                print("Company name and ticker are required. Please try again.")
                continue

            # Run the full investigation with all three parameters
            final_report = orchestrator.run_investigation(company_name, ticker, cik)

            # Print the final report
            print("\n--- FINAL PROFESSIONAL RISK ANALYSIS REPORT ---")
            # The report is already in Markdown, so we just print it.
            print(final_report)
            print("---------------------------------------------")
            
            # Ask the user if they want to investigate another company
            another = input("\nDo you want to investigate another company? (yes/no): ").lower()
            if another != 'yes':
                break

    except KeyboardInterrupt:
        print("\n\nExiting AutoInvestigator. Goodbye!")
    finally:
        print("\nAutoInvestigator session ended.")


if __name__ == '__main__':
    # Make sure the server is running in another terminal before starting the UI!
    main()