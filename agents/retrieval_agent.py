from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from utils.mcp import create_mcp_message

class RetrievalAgent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.db = None

    def build_vector_store(self, chunks):
        self.db = FAISS.from_documents(chunks, self.embeddings)

    def retrieve(self, query):
        docs = self.db.similarity_search(query, k=3)
        simplified = []
        for d in docs:
            content = d.page_content.strip()
            if not content:
                continue
            snippet = content.split('\n')
            shortened = " ".join(snippet[:2])[:300]
            simplified.append(shortened)
        if not simplified:
            simplified.append("⚠️ No relevant content found in the document.")
        return create_mcp_message("RetrievalAgent", "LLMResponseAgent", "RETRIEVAL_RESULT", {
            "retrieved_chunks": simplified,
            "query": query
        })
