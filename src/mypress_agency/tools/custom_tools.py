from crewai.tools import BaseTool
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
        Recupera conteúdo real da base de conhecimento usando LangChain e ChromaDB.
        """
        from mypress_agency.knowledge_manager import knowledge_manager
        
        print(f"Buscando informações na base de conhecimento para: {topic}...")
        context = knowledge_manager.query(topic)
        
        if "Base de conhecimento não inicializada" in context or not context.strip():
            return f"Aviso: Não foram encontradas informações específicas sobre '{topic}' na base de conhecimento local. Por favor, use seus conhecimentos gerais para criar o melhor conteúdo possível, mantendo o tom de voz da marca."
            
        return f"""
        [CONTEÚDO REAL EXTRAÍDO DA BASE DE CONHECIMENTO RAG]
        
        Tópico: {topic}
        
        Contexto Recuperado:
        {context}
        
        Instruções: Use os dados acima para fundamentar tecnicamente o post, garantindo que as informações sejam precisas e baseadas nos documentos fornecidos.
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
        "Ferramenta para gerar imagens reais usando a API da Stability AI. "
        "Recebe uma descrição detalhada e um estilo visual."
    )
    args_schema: Type[BaseModel] = ImageGeneratorToolSchema

    def _run(self, description: str, style: str) -> str:
        """
        Gera uma imagem de fundo via Stability AI e aplica o template de marca localmente.
        """
        import os
        import requests
        import base64
        from datetime import datetime
        from dotenv import load_dotenv
        from mypress_agency.image_processor import image_processor

        load_dotenv()
        api_key = os.getenv("STABILITY_API_KEY")
        
        if not api_key or api_key == "SUA_STABILITY_KEY_AQUI":
            return f"Erro: STABILITY_API_KEY não configurada. Simulação de imagem para: {description}"

        print(f"Gerando fundo da imagem via Stability AI...")
        
        engine_id = "stable-diffusion-v1-6"
        api_host = "https://api.stability.ai"

        # Prompt focado apenas no fundo técnico, sem tentar gerar texto
        clean_prompt = f"{description}, technical laboratory background, clean composition, high resolution"

        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [{"text": clean_prompt, "weight": 1}],
                "cfg_scale": 7,
                "height": 512,
                "width": 512,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code != 200:
            return f"Erro na API da Stability AI: {response.text}"

        # Salva o fundo temporário
        temp_bg = "outputs/images/temp_bg.png"
        os.makedirs("outputs/images", exist_ok=True)
        
        data = response.json()
        with open(temp_bg, "wb") as f:
            f.write(base64.b64decode(data["artifacts"][0]["base64"]))

        # Aplica o Template de Marca (Composição Híbrida)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"branded_cover_{timestamp}.png"
        final_path = os.path.join("outputs/images", final_filename)
        
        # O título para a imagem será extraído do contexto ou simplificado da descrição
        image_title = description.split('.')[0][:30] # Pega a primeira frase curta
        
        image_processor.create_branded_cover(temp_bg, image_title, final_path)
        
        # Remove o fundo temporário
        if os.path.exists(temp_bg):
            os.remove(temp_bg)

        return f"""
        [CAPA PADRONIZADA GERADA COM SUCESSO]
        
        Título Aplicado: {image_title}
        Caminho Final: {final_path}
        
        A imagem segue o padrão visual da marca (Cores, Fontes e Layout).
        """

# Instâncias das ferramentas
rag_retriever_tool = RAGContentRetrieverTool()
wp_publisher_tool = WordPressPublisherTool()
image_generator_tool = ImageGeneratorTool()
