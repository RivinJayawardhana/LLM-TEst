# Step 1: Install Required Libraries
# pip install transformers flask torch

from flask import Flask, request, jsonify
from transformers import pipeline

# Step 2: Load a Pre-Trained Model and Fine-Tune It
# Using a Question Answering pipeline (e.g., BERT or DistilBERT)
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Step 3: Define Your Company Data (FAQs)
context = """
Our company, TechSolutions, specializes in providing cutting-edge software solutions for businesses worldwide. 
Founded in 2010, we offer services including cloud computing, AI development, and data analytics. 
Our headquarters are located in New York City, and we have offices in London and Tokyo. 
For support, contact support@techsolutions.com or call +1-800-555-1234.
"""

# Step 4: Set Up the Flask App
app = Flask(__name__)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get("question")
    if not user_input:
        return jsonify({"error": "Question not provided."}), 400

    try:
        # Generate the answer using the QA pipeline
        result = qa_pipeline({"question": user_input, "context": context})
        return jsonify({"answer": result["answer"], "score": result["score"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Step 5: Frontend Code
frontend_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Company Chatbot</title>
    <script>
        async function askQuestion() {
            const question = document.getElementById('question').value;
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });
            const data = await response.json();
            document.getElementById('answer').innerText = data.answer || data.error;
        }
    </script>
</head>
<body>
    <h1>Welcome to TechSolutions Chatbot</h1>
    <input type="text" id="question" placeholder="Ask a question about TechSolutions">
    <button onclick="askQuestion()">Submit</button>
    <p id="answer"></p>
</body>
</html>
"""

@app.route('/')
def frontend():
    return frontend_code

# Step 6: Run the App
if __name__ == "__main__":
    app.run(debug=True, port=5000)
