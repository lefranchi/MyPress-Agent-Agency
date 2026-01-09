# 🚀 MyPress-Agent-Agency

Uma agência de conteúdo multi-agente autônoma, desenvolvida com **CrewAI**, projetada para transformar documentos técnicos em posts de alta qualidade para WordPress. O sistema utiliza **RAG (Retrieval-Augmented Generation)** para garantir que o conteúdo seja tecnicamente preciso e baseado na sua própria base de conhecimento.

## 🌟 Funcionalidades Principais

- **🤖 8 Agentes Especializados**: Um workflow completo que vai desde a estratégia de conteúdo e SEO até a revisão final e design.
- **🧠 RAG Real (LangChain + ChromaDB)**: O sistema lê seus PDFs, arquivos de texto e Markdown para fundamentar os artigos.
- **🎯 Seleção Dinâmica de Temas**: O sistema analisa sua base de conhecimento e sugere temas relevantes automaticamente.
- **🚫 Controle de Histórico**: Evita a repetição de temas já publicados através de um rastreador de histórico (`published_topics.txt`).
- **🎨 Geração de Imagens (Stability AI)**: Criação automática de imagens de destaque usando IA generativa.
- **📦 Exportação Local**: Salva automaticamente o artigo final (Markdown) e a imagem gerada em pastas organizadas (`outputs/`).
- **⚡ Gerenciamento com UV**: Utiliza o `uv` para um ambiente Python extremamente rápido e consistente.

## 🏗️ Estrutura do Projeto

```text
MyPress-Agent-Agency/
├── src/mypress_agency/
│   ├── config/          # Configurações YAML de Agentes e Tarefas
│   ├── tools/           # Ferramentas customizadas (RAG, WP, Stability)
│   ├── crew.py          # Orquestração da Crew
│   ├── main.py          # Ponto de entrada e lógica de temas
│   └── knowledge_manager.py # Gerenciamento do RAG
├── knowledge_base/      # Coloque seus documentos aqui (PDF, TXT, MD)
├── outputs/             # Artigos e imagens gerados
├── chroma_db/           # Banco de vetores local
└── pyproject.toml       # Dependências e scripts (uv)
```

## 🛠️ Configuração e Instalação

### 1. Pré-requisitos
- Python 3.10+
- [uv](https://astral.sh/uv/) instalado

### 2. Instalação
```bash
git clone https://github.com/lefranchi/MyPress-Agent-Agency.git
cd MyPress-Agent-Agency
```

### 3. Configuração de Ambiente
Crie um arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
```
Preencha as chaves necessárias:
- `OPENAI_API_KEY`: Para os agentes e embeddings.
- `STABILITY_API_KEY`: Para a geração de imagens.

### 4. Alimente a Base de Conhecimento
Coloque seus documentos técnicos na pasta `knowledge_base/`. O sistema aceita `.pdf`, `.txt` e `.md`.

## 🚀 Como Executar

Para iniciar a agência e gerar um post:
```bash
uv run mypress-agency
```

O sistema irá:
1. Indexar seus documentos.
2. Sugerir um tema inédito baseado no conteúdo.
3. Executar o workflow dos 8 agentes.
4. Salvar o artigo e a imagem na pasta `outputs/`.

## 👥 Os Agentes

| Agente | Responsabilidade | Ferramenta |
| :--- | :--- | :--- |
| **Estrategista** | Define persona e extrai contexto do RAG. | `RAGContentRetrieverTool` |
| **SEO Specialist** | Otimiza palavras-chave e estrutura H1-H3. | Nenhuma |
| **Copywriter** | Redige o artigo técnico e persuasivo. | Nenhuma |
| **Editor** | Garante fluidez e qualidade editorial. | Nenhuma |
| **Revisor** | Correção gramatical e ortográfica final. | Nenhuma |
| **Designer** | Cria o prompt e gera a imagem de destaque. | `ImageGeneratorTool` (Stability AI) |
| **Social Media** | Cria chamadas para redes sociais. | Nenhuma |
| **Publisher** | Prepara a publicação final. | `WordPressPublisherTool` |

## 💡 Próximos Passos

- [ ] **Integração Real WordPress**: Atualmente a ferramenta de publicação simula o envio. Você pode atualizar `custom_tools.py` para usar a API REST real do WordPress.
- [ ] **Suporte a mais formatos**: Adicionar suporte para busca em URLs e vídeos do YouTube.

---
Desenvolvido com ❤️ para automação inteligente de conteúdo.
