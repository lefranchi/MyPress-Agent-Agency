# ManusPress-Agent-Agency

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

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/SEU_USUARIO/ManusPress-Agent-Agency.git
    cd ManusPress-Agent-Agency
    ```

2.  **Crie o Ambiente Virtual e Instale as Dependências:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure as Chaves de API:**
    Renomeie o arquivo `.env.example` para `.env` e preencha com sua chave de API da OpenAI (ou outro LLM compatível):
    ```bash
    mv .env.example .env
    # Edite o arquivo .env
    ```

4.  **Execução:**
    Execute o script principal para iniciar a agência:
    ```bash
    python3 agency_crew.py
    ```

### 💡 Próximos Passos (Customização)

As ferramentas (`tools.py`) estão atualmente em modo de simulação (placeholder). Para uma implementação completa, você precisará:

1.  **Implementar o RAG Real:** Substituir o `_run` da `RAGContentRetrieverTool` por uma lógica que use LangChain/LlamaIndex para buscar em seus documentos reais.
2.  **Integrar a Publicação no WP:** Substituir o `_run` da `WordPressPublisherTool` para fazer chamadas reais à API REST do WordPress.
3.  **Integrar a Geração de Imagem:** Substituir o `_run` da `ImageGeneratorTool` para chamar uma API de geração de imagem (ex: DALL-E, Midjourney).
