from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import os
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

ingestion_agent = IngestionAgent()
retriever = RetrievalAgent()
llm_agent = LLMResponseAgent()

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []
    if "stored_chunks" not in session:
        session["stored_chunks"] = []
    warning = None
    answer = None
    source_chunks = []

    if request.method == "POST":
        file = request.files.get("file")
        query = request.form.get("query")

        if file:
            parsed_result = ingestion_agent.ingest(file)
            documents = parsed_result["payload"]["chunks"]
            session["stored_chunks"] = documents
            retriever.build_vector_store(documents)
        elif session.get("stored_chunks"):
            retriever.build_vector_store(session["stored_chunks"])

        if not session.get("stored_chunks"):
            warning = "⚠️ Please upload a document before asking questions."
        elif query:
            retrieved = retriever.retrieve(query)
            chunks = retrieved["payload"]["retrieved_chunks"]
            response_msg = llm_agent.respond(chunks, query)
            answer = response_msg["payload"]["answer"]
            source_chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 30]
            if not source_chunks or all("⚠️" in chunk or len(chunk.split()) < 5 for chunk in source_chunks):
                source_chunks = ["⚠️ Source content could not be extracted clearly from this document."]
            session["chat_history"].append({"role": "user", "text": query})
            session["chat_history"].append({"role": "bot", "text": answer})
            session.modified = True

    return render_template("index.html", history=session["chat_history"], sources=source_chunks, warning=warning)

@app.route("/clear", methods=["POST"])
def clear():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
