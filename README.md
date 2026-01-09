# MyPress-Agent-Agency

## Agência de Conteúdo Multi-Agente para WordPress com RAG (CrewAI)

Este projeto implementa um sistema multi-agente utilizando o framework **CrewAI** para automatizar a criação de posts de alta qualidade para o WordPress, utilizando uma Base de Conhecimento (RAG - Retrieval-Augmented Generation) como fonte primária de informação.

O sistema simula uma agência de conteúdo completa, com 8 agentes especializados que trabalham em um fluxo sequencial para garantir a qualidade e a otimização do conteúdo.

### 🚀 Workflow da Agência

O processo é dividido em 8 etapas, cada uma executada por um agente especializado:

| ID | Agente | Função Principal | Ferramentas |
| :---: | :--- | :--- | :--- |
| 1 | **Estrategista de Conteúdo** | Define o briefing e extrai o conteúdo base da Base de Conhecimento (RAG). | `RAGContentRetrieverTool` |
| 2 | **SEO Specialist** | Otimiza o briefing, define palavras-chave, estrutura de headings e metadados de SEO. | Nenhuma (Usa contexto) |
| 3 | **Copywriter** | Redige o artigo completo com base no conteúdo RAG e no plano de SEO. | Nenhuma (Usa contexto) |
| 4 | **Editor de Conteúdo** | Revisa a estrutura, lógica e fluidez do rascunho. | Nenhuma (Usa contexto) |
| 5 | **Revisor** | Realiza a revisão final de gramática, ortografia e pontuação. | Nenhuma (Usa contexto) |
| 6 | **Designer de Conteúdo** | Cria o prompt para a geração de imagem/infográfico de destaque. | `ImageGeneratorTool` |
| 7 | **Social Media Manager** | Adapta o conteúdo para copies de divulgação em redes sociais. | Nenhuma (Usa contexto) |
| 8 | **Publisher** | Publica o artigo final no WordPress, aplicando formatação e metadados. | `WordPressPublisherTool` |

### 🛠️ Configuração e Instalação

Este projeto utiliza o **uv** para um gerenciamento de dependências extremamente rápido e moderno.

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/lefranchi/MyPress-Agent-Agency.git
    cd MyPress-Agent-Agency
    ```

2.  **Instale o uv (se ainda não tiver):**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3.  **Configure as Chaves de API:**
    Renomeie o arquivo `.env.example` para `.env` e preencha com sua chave de API da OpenAI:
    ```bash
    cp .env.example .env
    ```

4.  **Execução:**
    Para rodar a agência, basta usar o comando:
    ```bash
    uv run src/mypress_agency/main.py
    ```

### 📂 Estrutura do Projeto

O projeto segue as melhores práticas do CrewAI, utilizando arquivos YAML para configuração:

- `src/mypress_agency/config/agents.yaml`: Definição de personas, metas e backstories.
- `src/mypress_agency/config/tasks.yaml`: Definição das tarefas e fluxos de trabalho.
- `src/mypress_agency/crew.py`: Lógica de orquestração da Crew.
- `src/mypress_agency/tools/`: Ferramentas customizadas (RAG, WordPress, Imagens).

### 🧠 Base de Conhecimento (RAG Real)

O projeto agora conta com uma implementação real de RAG utilizando **LangChain** e **ChromaDB**.

1.  **Como usar:**
    *   Coloque seus documentos técnicos (PDF, TXT ou MD) na pasta `knowledge_base/`.
    *   Ao rodar o sistema, ele irá indexar automaticamente esses documentos em um banco de vetores local (`chroma_db/`).
    *   O **Estrategista de Conteúdo** usará esses documentos para fundamentar todos os posts criados.

### 💡 Próximos Passos (Customização)

As ferramentas de publicação e imagem ainda estão em modo de simulação. Para completar a automação:

1.  **Integrar a Publicação no WP:** No arquivo `src/mypress_agency/tools/custom_tools.py`, atualize a classe `WordPressPublisherTool` para fazer chamadas reais à API REST do WordPress usando as credenciais do seu `.env`.
2.  **Integrar a Geração de Imagem:** Atualize a classe `ImageGeneratorTool` para chamar uma API como DALL-E 3 ou Midjourney.
