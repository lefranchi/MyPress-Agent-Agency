import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from dotenv import load_dotenv
from tools import rag_retriever_tool, wp_publisher_tool, image_generator_tool

# Carrega variáveis de ambiente (como as chaves de API)
load_dotenv()

# Configuração do LLM (Usando OpenAI como padrão, mas pode ser alterado)
# Certifique-se de que a variável de ambiente OPENAI_API_KEY está configurada
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini" # Modelo eficiente para esta tarefa

# --- 1. Definição dos Agentes ---

# 1. Estrategista de Conteúdo
content_strategist = Agent(
    role='Estrategista de Conteúdo Sênior',
    goal='Definir a estratégia de conteúdo, persona-alvo, tom de voz e extrair o conteúdo base da Base de Conhecimento (RAG).',
    backstory=(
        "Você é um estrategista de marketing com 10 anos de experiência, especialista em alinhar "
        "conteúdo técnico com objetivos de negócio. Sua primeira missão é usar a ferramenta RAG "
        "para extrair o contexto necessário e criar um briefing detalhado."
    ),
    tools=[rag_retriever_tool],
    verbose=True,
    allow_delegation=False
)

# 2. SEO Specialist
seo_specialist = Agent(
    role='Especialista em SEO On-Page e Otimização',
    goal='Otimizar o briefing e o conteúdo RAG com palavras-chave, estrutura de headings (H1-H3), meta title e meta description.',
    backstory=(
        "Você é um guru de SEO, focado em intenção de busca e ranqueamento orgânico. "
        "Você transforma um briefing em um plano de SEO executável."
    ),
    verbose=True,
    allow_delegation=False
)

# 3. Copywriter / Content Writer
copywriter = Agent(
    role='Copywriter Persuasivo e Escritor Técnico',
    goal='Redigir um artigo completo, claro e envolvente, aplicando técnicas de copywriting e incorporando o plano de SEO.',
    backstory=(
        "Você é um escritor versátil, capaz de pegar informações técnicas e transformá-las em "
        "textos que engajam e convertem, mantendo o tom de voz definido pelo Estrategista."
    ),
    verbose=True,
    allow_delegation=False
)

# 4. Editor de Conteúdo
content_editor = Agent(
    role='Editor de Conteúdo e Qualidade Editorial',
    goal='Revisar a estrutura, lógica, fluidez e coerência argumentativa do rascunho do artigo.',
    backstory=(
        "Você é o guardião da qualidade editorial. Sua missão é garantir que o artigo seja "
        "impecável em sua narrativa e aderência ao briefing inicial."
    ),
    verbose=True,
    allow_delegation=False
)

# 5. Revisor (Proofreader)
proofreader = Agent(
    role='Revisor Gramatical e Linguístico',
    goal='Realizar a revisão final de gramática, ortografia e pontuação, eliminando qualquer erro linguístico.',
    backstory=(
        "Você é um revisor meticuloso, com um olho de águia para erros. Seu trabalho é o polimento final, "
        "garantindo que o texto esteja perfeito para publicação."
    ),
    verbose=True,
    allow_delegation=False
)

# 6. Designer de Conteúdo
designer = Agent(
    role='Designer de Conteúdo e Criador de Imagens',
    goal='Criar uma descrição detalhada para a geração de uma imagem/infográfico que ilustre o artigo.',
    backstory=(
        "Você é um designer que entende de marketing. Sua tarefa é traduzir o conceito central do artigo "
        "em um prompt visual para a ferramenta de geração de imagens."
    ),
    tools=[image_generator_tool],
    verbose=True,
    allow_delegation=False
)

# 7. Social Media Manager
social_media_manager = Agent(
    role='Especialista em Divulgação e Engajamento Social',
    goal='Adaptar o conteúdo final para chamadas e formatos de divulgação em redes sociais (LinkedIn, Instagram, etc.).',
    backstory=(
        "Você é o responsável por levar o conteúdo para o público certo nas redes sociais, "
        "criando copies curtas e chamativas com hashtags relevantes."
    ),
    verbose=True,
    allow_delegation=False
)

# 8. Publisher / Web Content Manager
publisher = Agent(
    role='Web Content Manager e Publicador WordPress',
    goal='Publicar o artigo final, formatado e com todos os metadados, no WordPress.',
    backstory=(
        "Você é o responsável pela etapa final. Garante que o artigo, o SEO, as imagens e as chamadas sociais "
        "estejam integrados e prontos para o CMS, usando a ferramenta de publicação."
    ),
    tools=[wp_publisher_tool],
    verbose=True,
    allow_delegation=True # Pode delegar a checagem final para o Editor, se necessário
)

# --- 2. Definição das Tarefas ---

# Tópico de Exemplo (O usuário fornecerá isso)
TOPIC = "A Revolução dos Sistemas Multi-Agente na Automação de Conteúdo para WordPress"

task_1 = Task(
    description=f"1. Definir o objetivo, persona, tom de voz (autoritário e inspirador) e mensagem central para o tópico: '{TOPIC}'. "
                "2. Usar a ferramenta `RAG Content Retriever Tool` para extrair o conteúdo técnico da base de conhecimento. "
                "O resultado deve ser um Briefing detalhado contendo: Objetivo, Persona, Tom de Voz, Mensagem Central e o Conteúdo RAG extraído.",
    agent=content_strategist,
    expected_output="Um Briefing de Conteúdo completo e o Conteúdo RAG extraído, prontos para o SEO Specialist."
)

task_2 = Task(
    description="Com base no Briefing e no Conteúdo RAG, realizar a pesquisa de palavras-chave (simulada) e definir a estrutura de SEO. "
                "O resultado deve ser um Plano de SEO contendo: Palavra-chave Principal, Intenção de Busca, Estrutura de Headings (H1, H2, H3) e rascunhos de Meta Title e Meta Description.",
    agent=seo_specialist,
    context=[task_1],
    expected_output="Um Plano de SEO detalhado, pronto para ser usado pelo Copywriter."
)

task_3 = Task(
    description="Redigir o artigo completo (mínimo 800 palavras) usando o Conteúdo RAG como base e seguindo estritamente o Plano de SEO. "
                "Focar em clareza, persuasão e valor para o leitor, mantendo o tom de voz definido.",
    agent=copywriter,
    context=[task_2],
    expected_output="O rascunho inicial do artigo em formato Markdown."
)

task_4 = Task(
    description="Revisar o rascunho do artigo. Focar na estrutura, lógica, fluidez, coerência argumentativa e aderência ao Briefing original. "
                "O resultado deve ser um rascunho refinado, pronto para a revisão final de gramática.",
    agent=content_editor,
    context=[task_3],
    expected_output="O rascunho refinado do artigo, com melhorias editoriais e estruturais."
)

task_5 = Task(
    description="Realizar a revisão final (Proofreading) do rascunho refinado. Corrigir erros gramaticais, ortográficos e de pontuação. "
                "O resultado deve ser o Artigo Final, pronto para publicação.",
    agent=proofreader,
    context=[task_4],
    expected_output="O Artigo Final, 100% livre de erros e pronto para ser publicado."
)

task_6 = Task(
    description="Criar um prompt detalhado para a ferramenta `Image Generator Tool` que resulte em um infográfico ou imagem de destaque para o artigo. "
                "O resultado deve ser a descrição da imagem gerada e o caminho do arquivo (simulado).",
    agent=designer,
    context=[task_5],
    expected_output="A descrição da imagem gerada e o caminho do arquivo (simulado) para o Publisher."
)

task_7 = Task(
    description="Com base no Artigo Final, criar 3 variações de copy para redes sociais (LinkedIn, Instagram e X/Twitter), incluindo hashtags relevantes e uma chamada para ação (CTA).",
    agent=social_media_manager,
    context=[task_5],
    expected_output="Um bloco de texto contendo as 3 copies de redes sociais formatadas."
)

task_8 = Task(
    description="Usar o Artigo Final, o Plano de SEO e a ferramenta `WordPress Publisher Tool` para simular a publicação do post no WordPress. "
                "O Publisher deve reunir o Título (do Plano de SEO), o Conteúdo (do Artigo Final) e os Metadados (do Plano de SEO e Social Media Copy) e executar a publicação.",
    agent=publisher,
    context=[task_5, task_2, task_7],
    expected_output="A confirmação da publicação no WordPress (URL de rascunho) e um resumo de todo o processo."
)

# --- 3. Orquestração da Crew ---

# A ordem das tarefas é sequencial, com a Task 8 dependendo de várias tarefas anteriores.
# A Task 6 e 7 podem rodar em paralelo com a Task 5.
crew = Crew(
    agents=[
        content_strategist,
        seo_specialist,
        copywriter,
        content_editor,
        proofreader,
        designer,
        social_media_manager,
        publisher
    ],
    tasks=[task_1, task_2, task_3, task_4, task_5, task_6, task_7, task_8],
    process=Process.sequential, # Processo sequencial para garantir a qualidade
    verbose=2, # Nível de detalhe alto
)

# --- 4. Execução da Crew ---

print("--- Iniciando a Agência de Conteúdo Multi-Agente (MyPress-Agent-Agency) ---")
result = crew.kickoff(inputs={'topic': TOPIC})

print("\n\n################################################")
print("############# RESULTADO FINAL DA CREW #############")
print("################################################\n")
print(result)
