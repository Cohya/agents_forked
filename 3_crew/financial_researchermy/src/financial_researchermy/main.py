#!/usr/bin/env python
import sys
import warnings
import os 
from datetime import datetime

from financial_researchermy.crew import FinancialResearchermy

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'company': 'Tesla'
    }
    # Preflight check for OpenAI API key (read by crewai via dotenv or env)

    result = FinancialResearchermy().crew().kickoff(inputs=inputs)
    print(result.raw)
 

if __name__ == "__main__":
    run()