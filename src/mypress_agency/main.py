#!/usr/bin/env python
import sys
from mypress_agency.crew import MyPressAgencyCrew

def run():
    """
    Run the crew.
    """
    from mypress_agency.knowledge_manager import knowledge_manager
    
    print("--- Inicializando Base de Conhecimento (RAG) ---")
    # Carrega e indexa os documentos da pasta 'knowledge_base'
    knowledge_manager.load_and_index()
    
    inputs = {
        'topic': 'A Revolução dos Sistemas Multi-Agente na Automação de Conteúdo para WordPress'
    }
    
    print("--- Iniciando a Agência de Conteúdo Multi-Agente (MyPress-Agent-Agency) ---")
    MyPressAgencyCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
