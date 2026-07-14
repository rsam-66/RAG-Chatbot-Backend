from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import logging
import requests
import os

logger = logging.getLogger(__name__)

PERSIST_DIRECTORY = "chroma_db"
# OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434") Temporary change from ollama:11434 to localhost:11434 for testing performance
OLLAMA_URL = os.getenv("OLLAMA_URL", "OLLAMA_URL=http://ollama:11434")

print("DEBUG OLLAMA_URL =", OLLAMA_URL)

# Prompt to ensure all answers are in Indonesian and use context/history effectively
INDO_PROMPT = PromptTemplate(
    input_variables=["context", "question", "history"],
    template="""
    Anda adalah asisten wisata Pangandaran.

    ATURAN WAJIB:
    - Jawab SELALU dalam Bahasa Indonesia.
    - Jangan gunakan Bahasa Inggris.
    - Gunakan konteks dokumen dan riwayat percakapan untuk menjawab.

    Riwayat Percakapan:
    {history}

    Konteks Dokumen:
    {context}

    Pertanyaan Pengguna:
    {question}

    Jawaban dalam Bahasa Indonesia:
    """
)

class RAGChatbot:
    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        self.vectordb = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=self.embedding
        )

        # Retrieve lebih banyak dokumen untuk coverage yang lebih baik
        self.retriever = self.vectordb.as_retriever(search_kwargs={"k": 7})

        # Check jika Ollama available
        self.ollama_available = self._check_ollama()
        
        if self.ollama_available:
            self.llm = Ollama(
                base_url=OLLAMA_URL,
                model="mistral",
                temperature=0.0,
            )
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=self.retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": INDO_PROMPT}
            )
            logger.info("Ollama LLM initialized successfully")
        else:
            self.qa_chain = None
            logger.warning("Ollama not available. Using fallback mode. Please start Ollama: 'ollama serve'")

    def _check_ollama(self):
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama check failed: {str(e)}")
            return False

    def ask(self, query: str, history: str = ""):

        # If ollama unavailable, return error message instead of trying to run the chain
        if not self.ollama_available:
            return {
                "answer": "Ollama tidak tersedia",
                "sources": [],
                "metadata": []
            }

        try:
            docs = self.vectordb.similarity_search(query, k=7)

            context = "\n\n".join([doc.page_content for doc in docs])

            prompt = INDO_PROMPT.format(
                context=context,
                question=query,
                history=history
            )

            answer = self.llm.invoke(prompt)

            # Extract metadata from retrieved documents
            metadata_list = []
            for doc in docs:
                if hasattr(doc, 'metadata') and doc.metadata:
                    metadata_list.append(doc.metadata)

            return {
                "answer": answer,
                "sources": list(set(doc.page_content for doc in docs)),
                "metadata": metadata_list
            }

        except Exception as e:
            logger.error(f"Chat error: {str(e)}", exc_info=True)

            return {
                "answer": f"Error: {str(e)}",
                "sources": [],
                "metadata": []
            }