#!/usr/bin/env python
import sys
import warnings

from crew import AgenticPdfRag

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """

    user_input = input("Enter your question: ")

    inputs = {
        'input': user_input
    }

    result = AgenticPdfRag().crew().kickoff(inputs=inputs)
    print(result)

if __name__ == "__main__":
    run()