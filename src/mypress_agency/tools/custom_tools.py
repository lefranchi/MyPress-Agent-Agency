from crewai_tools import BaseTool
from typing import Any, Type
from pydantic import BaseModel, Field

# --- Ferramentas Customizadas ---

class RAGContentRetrieverToolSchema(BaseModel):
    """Schema para a ferramenta de recuperação de conteúdo RAG."""
    topic: str = Field(description="O tópico principal para o qual o conteúdo deve ser recuperado.")

class RAGContentRetrieverTool(BaseTool):
    name: str = "RAG Content Retriever Tool"
    description: str = (
        "Ferramenta para buscar e extrair informações detalhadas de uma Base de Conhecimento (RAG) "
        "com documentos técnicos e contextuais. Use esta ferramenta para obter o conteúdo base "
        "necessário para a criação do post."
    )
    args_schema: Type[BaseModel] = RAGContentRetrieverToolSchema

    def _run(self, topic: str) -> str:
        """
        Simula a recuperação de conteúdo de uma base RAG.
        Em uma implementação real, este método usaria LangChain para:
        1. Carregar documentos (PDFs, Markdown, etc.)
        2. Criar embeddings e armazenar em um Vector Store (ex: ChromaDB)
        3. Realizar uma busca por similaridade com o 'topic'
        4. Retornar o conteúdo relevante.
        """
        # Placeholder para simular o conteúdo extraído da base de conhecimento
        return f"""
        [CONTEÚDO EXTRAÍDO DA BASE DE CONHECIMENTO RAG PARA O TÓPICO: {topic}]

        **Mensagem Central:** A adoção de sistemas multi-agente baseados em CrewAI revoluciona a automação de marketing de conteúdo, permitindo a criação de posts de alta qualidade, otimizados para SEO e com base em dados internos (RAG), garantindo consistência e autoridade da marca.

        **Dados Técnicos:**
        - Framework: CrewAI (Python)
        - Orquestração: 8 agentes especializados (Estrategista, SEO, Copywriter, Editor, Revisor, Designer, Social Media, Publisher).
        - Integração: WordPress API REST (para publicação) e Vector Store (para RAG).
        - Benefício Principal: Redução de 80% no tempo de produção de conteúdo e aumento de 40% no engajamento orgânico devido à otimização de SEO e qualidade editorial.

        **Contexto Adicional:** O sistema deve ser capaz de lidar com a complexidade de documentos técnicos, transformando-os em linguagem acessível para o público-alvo (persona: Pequenos e Médios Empresários). O tom de voz deve ser informativo, autoritário e inspirador.
        """

class WordPressPublisherToolSchema(BaseModel):
    """Schema para a ferramenta de publicação no WordPress."""
    title: str = Field(description="O título final do post.")
    content: str = Field(description="O conteúdo final do post em formato HTML ou Markdown.")
    metadata: str = Field(description="Metadados de SEO (meta description, tags, categorias).")

class WordPressPublisherTool(BaseTool):
    name: str = "WordPress Publisher Tool"
    description: str = (
        "Ferramenta para publicar o conteúdo final no WordPress via API REST. "
        "Recebe o título, o conteúdo formatado e os metadados de SEO."
    )
    args_schema: Type[BaseModel] = WordPressPublisherToolSchema

    def _run(self, title: str, content: str, metadata: str) -> str:
        """
        Simula a publicação do post no WordPress.
        Em uma implementação real, este método usaria a biblioteca `python-wordpress-xmlrpc`
        ou faria requisições HTTP para a API REST do WordPress.
        """
        # Placeholder para simular a publicação
        return f"""
        [POST PUBLICADO COM SUCESSO NO WORDPRESS]
        
        Título: {title}
        Status: Rascunho (Draft)
        URL de Pré-visualização: https://seusite.com/preview/{title.lower().replace(' ', '-')}-draft
        Metadados Aplicados: {metadata}
        
        Aguardando aprovação final do Web Content Manager.
        """

class ImageGeneratorToolSchema(BaseModel):
    """Schema para a ferramenta de geração de imagem."""
    description: str = Field(description="Descrição detalhada da imagem a ser gerada.")
    style: str = Field(description="Estilo visual desejado (ex: infográfico, ilustração minimalista).")

class ImageGeneratorTool(BaseTool):
    name: str = "Image Generator Tool"
    description: str = (
        "Ferramenta para gerar imagens, ilustrações ou gráficos para acompanhar o post. "
        "Use-a para criar um visual atraente e relevante."
    )
    args_schema: Type[BaseModel] = ImageGeneratorToolSchema

    def _run(self, description: str, style: str) -> str:
        """
        Simula a geração de imagem.
        Em uma implementação real, este método chamaria uma API de geração de imagem (ex: DALL-E, Midjourney).
        """
        # Placeholder para simular a geração de imagem
        return f"""
        [IMAGEM GERADA COM SUCESSO]
        
        Descrição: {description}
        Estilo: {style}
        Caminho do Arquivo: /assets/images/post-image-{hash(description)}.png
        
        A imagem está pronta para ser inserida no post.
        """

# Instâncias das ferramentas
rag_retriever_tool = RAGContentRetrieverTool()
wp_publisher_tool = WordPressPublisherTool()
image_generator_tool = ImageGeneratorTool()
