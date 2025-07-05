from langchain_openai.chat_models import ChatOpenAI
from utils.mcp import create_mcp_message

class LLMResponseAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    def respond(self, context_chunks, query):
        context = "\n\n".join(context_chunks)
        prompt = f"""Use the following context to answer the question:
{context}

Question: {query}
Answer:"""

        response = self.llm.predict(prompt)
        return create_mcp_message("LLMResponseAgent", "UI", "FINAL_ANSWER", {
            "answer": response,
            "source": context_chunks
        })