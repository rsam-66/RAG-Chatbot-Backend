from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import logging
import requests
import os

logger = logging.getLogger(__name__)

PERSIST_DIRECTORY = "chroma_db"

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
        
        # Initialize Groq LLM using the llama3 model
        self.llm = ChatGroq(
            model_name="llama3-8b-8192",
            temperature=0.0,
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": INDO_PROMPT}
        )
        logger.info("Groq LLM initialized successfully")

    def ask(self, query: str, history: str = ""):
        try:
            docs = self.vectordb.similarity_search(query, k=7)

            context = "\n\n".join([doc.page_content for doc in docs])

            prompt = INDO_PROMPT.format(
                context=context,
                question=query,
                history=history
            )

            answer = self.llm.invoke(prompt)
            
            # Since ChatGroq returns an AIMessage object, we need to extract the string content
            # If it's already a string, this will just use it as is.
            final_answer = answer.content if hasattr(answer, 'content') else answer

            # Extract metadata from retrieved documents
            metadata_list = []
            for doc in docs:
                if hasattr(doc, 'metadata') and doc.metadata:
                    metadata_list.append(doc.metadata)

            return {
                "answer": final_answer,
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