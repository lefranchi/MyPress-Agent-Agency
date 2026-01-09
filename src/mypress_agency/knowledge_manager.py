import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

class KnowledgeManager:
    def __init__(self, knowledge_dir: str = "knowledge_base", persist_dir: str = "chroma_db"):
        self.knowledge_dir = knowledge_dir
        self.persist_dir = persist_dir
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None

    def load_and_index(self):
        """Carrega documentos da pasta e cria o índice no ChromaDB."""
        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir)
            print(f"Diretório {self.knowledge_dir} criado. Adicione documentos lá.")
            return

        # Carregadores para diferentes tipos de arquivos
        loaders = {
            ".pdf": DirectoryLoader(self.knowledge_dir, glob="**/*.pdf", loader_cls=PyPDFLoader),
            ".txt": DirectoryLoader(self.knowledge_dir, glob="**/*.txt", loader_cls=TextLoader),
            ".md": DirectoryLoader(self.knowledge_dir, glob="**/*.md", loader_cls=TextLoader),
        }

        documents = []
        for ext, loader in loaders.items():
            documents.extend(loader.load())

        if not documents:
            print("Nenhum documento encontrado na base de conhecimento.")
            return

        # Divisão do texto em pedaços (chunks)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)

        # Criação e persistência do banco de vetores
        self.vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        print(f"Indexados {len(splits)} pedaços de {len(documents)} documentos.")

    def query(self, question: str, k: int = 3) -> str:
        """Realiza uma busca por similaridade na base de conhecimento."""
        if not self.vector_store:
            # Tenta carregar o banco persistido se ele existir
            if os.path.exists(self.persist_dir):
                self.vector_store = Chroma(
                    persist_directory=self.persist_dir,
                    embedding_function=self.embeddings
                )
            else:
                return "Base de conhecimento não inicializada ou vazia."

        results = self.vector_store.similarity_search(question, k=k)
        context = "\n\n".join([doc.page_content for doc in results])
        return context

    def suggest_topics(self) -> List[str]:
        """Sugere uma lista de tópicos baseada nos documentos indexados."""
        if not self.vector_store:
            if os.path.exists(self.persist_dir):
                self.vector_store = Chroma(
                    persist_directory=self.persist_dir,
                    embedding_function=self.embeddings
                )
            else:
                return []

        # Pega alguns documentos aleatórios para extrair temas
        # Como o Chroma não tem um 'get_random', pegamos os primeiros e usamos o LLM para sugerir temas
        docs = self.vector_store.get(limit=10)
        if not docs or not docs['documents']:
            return []

        combined_text = "\n".join(docs['documents'][:5])
        
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o-mini")
        
        prompt = f"""
        Com base no seguinte conteúdo extraído de uma base de conhecimento técnica:
        ---
        {combined_text}
        ---
        Sugira 5 temas específicos e interessantes para posts de blog. 
        Retorne apenas a lista de temas, um por linha, sem numeração ou explicações.
        """
        
        response = llm.invoke(prompt)
        topics = [t.strip() for t in response.content.strip().split('\n') if t.strip()]
        return topics

# Singleton para uso global
knowledge_manager = KnowledgeManager()
