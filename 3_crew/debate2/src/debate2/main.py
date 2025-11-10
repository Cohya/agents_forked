#!/usr/bin/env python
import sys
import os
import warnings

from datetime import datetime

from debate2.crew import Debate2

# Provide an early, user-friendly check for required API keys. The crew
# internals will also validate, but this gives an immediate actionable
# message during local runs.
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'motion': 'There needs to be strict laws to regulate LLMs',
    }
    # Preflight check for OpenAI API key (read by crewai via dotenv or env)
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Set it in your environment or create a .env file in the project root with 'OPENAI_API_KEY=your_key'.\n"
            "In PowerShell for this session run: $env:OPENAI_API_KEY=\"<your-key>\"\n"
            "To persist it for the current user (PowerShell): setx OPENAI_API_KEY \"<your-key>\"\n"
            "Do NOT commit your API key to version control. Add .env to .gitignore."
        )

    try:
        result = Debate2().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
