from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the QA model
model_name = "distilbert-base-cased-distilled-squad"
tokenizer = AutoTokenizer.from_pretrained(model_name)
qa_model = AutoModelForQuestionAnswering.from_pretrained(model_name)
qa_pipeline = pipeline("question-answering", model=qa_model, tokenizer=tokenizer)

# Company-related context documents (as examples for RAG)
company_documents = [
    "KmTec Ltd is a UK-based technology consultancy specializing in AI solutions and embedded systems, offering innovative services in human-machine interface (HMI) development, software integration, and IoT systems. The company provides custom solutions for industries including automotive, aerospace, healthcare, and telecommunications, with products such as smart water tank level detectors, queue management systems, and customer feedback platforms. KmTec Ltd also offers expertise in AI-powered chatbots, predictive models, and embedded systems design, leveraging technologies like Zigbee, STM8 microcontrollers, and advanced machine learning to help businesses optimize operations. With a focus on agile development, system engineering, and product lifecycle management, KmTec Ltd delivers tailored, high-performance solutions to meet complex business needs.",
]

# Create a retriever using TF-IDF
vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(company_documents)

def retrieve_relevant_document(question):
    """Retrieve the most relevant document using cosine similarity."""
    question_vector = vectorizer.transform([question])
    similarities = cosine_similarity(question_vector, doc_vectors).flatten()
    best_doc_index = np.argmax(similarities)
    return company_documents[best_doc_index]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        # Get the user's question from the request
        data = request.get_json()
        user_question = data.get("question", "")
        
        if not user_question:
            return jsonify({"error": "Question is required"}), 400
        
        # Retrieve the most relevant document
        relevant_context = retrieve_relevant_document(user_question)

        # Use the QA model to answer the question
        answer = qa_pipeline(question=user_question, context=relevant_context)
        
        # Return the answer
        return jsonify({"answer": answer["answer"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
