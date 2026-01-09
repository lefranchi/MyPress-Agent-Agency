#!/usr/bin/env python
import sys
from mypress_agency.crew import MyPressAgencyCrew

def run():
    """
    Run the crew.
    """
    import random
    import os
    from mypress_agency.knowledge_manager import knowledge_manager
    
    print("--- Inicializando Base de Conhecimento (RAG) ---")
    # Carrega e indexa os documentos da pasta 'knowledge_base'
    knowledge_manager.load_and_index()
    
    # --- Lógica de Seleção de Tema Dinâmico ---
    print("--- Selecionando Tema Baseado no Conteúdo ---")
    suggested_topics = knowledge_manager.suggest_topics()
    
    if not suggested_topics:
        print("Aviso: Não foi possível extrair temas da base de conhecimento. Usando tema padrão.")
        selected_topic = "Avanços na Engenharia de Materiais e Metalografia"
    else:
        # Carrega histórico de temas publicados
        history_file = "published_topics.txt"
        published_topics = []
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                published_topics = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
        
        # Filtra temas que ainda não foram publicados
        available_topics = [t for t in suggested_topics if t not in published_topics]
        
        if not available_topics:
            print("Todos os temas sugeridos já foram publicados. Reiniciando ciclo.")
            available_topics = suggested_topics
            
        selected_topic = random.choice(available_topics)
        
        # Salva o tema escolhido no histórico
        with open(history_file, "a") as f:
            f.write(f"{selected_topic}\n")

    print(f"TEMA SELECIONADO: {selected_topic}")
    
    inputs = {
        'topic': selected_topic
    }
    
    print("--- Iniciando a Agência de Conteúdo Multi-Agente (MyPress-Agent-Agency) ---")
    result = MyPressAgencyCrew().crew().kickoff(inputs=inputs)
    
    # --- Exportação Local do Artigo ---
    output_dir = "outputs/articles"
    os.makedirs(output_dir, exist_ok=True)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join([c if c.isalnum() else "_" for c in selected_topic])
    filename = f"article_{timestamp}_{safe_topic[:30]}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w") as f:
        f.write(f"# Tópico: {selected_topic}\n\n")
        f.write(str(result))
        
    print(f"\n--- PROCESSO CONCLUÍDO ---")
    print(f"Artigo salvo em: {filepath}")
    print(f"Imagens (se geradas) salvas em: outputs/images/")

if __name__ == "__main__":
    run()
