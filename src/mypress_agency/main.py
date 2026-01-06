#!/usr/bin/env python
import sys
from mypress_agency.crew import MyPressAgencyCrew

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'A Revolução dos Sistemas Multi-Agente na Automação de Conteúdo para WordPress'
    }
    MyPressAgencyCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
