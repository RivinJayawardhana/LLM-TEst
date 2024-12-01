# Step 1: Install Required Libraries
# pip install transformers flask torch

from flask import Flask, request, jsonify
from transformers import pipeline

# Step 2: Load a Pre-Trained Model and Fine-Tune It
# Using a Question Answering pipeline (e.g., BERT or DistilBERT)
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Step 3: Define Your Company Data (FAQs)
context = """
Kmtec Ltd is a UK-based AI consultancy offering a range of services including AI solutions, software integration, embedded systems, and web/app development. Their AI offerings focus on human-like AI chatbots, enabling businesses to enhance customer support with automated systems. They also provide specialized technical consultancy, including HMI development, test automation, and systems integration.

Kmtec Ltd’s portfolio includes innovative products like a Water Tank Level Detector, Queue Management Systems, and customer feedback solutions. They also offer tailored training programs in areas such as CAD, Electric Vehicle Powertrains, and software tools like Windchill PDMLink and FreeCAD.

The company specializes in developing software for industries like automotive, aerospace, and healthcare. Key services include system development, Agile software solutions, and technical architecture for projects requiring high compliance standards (ASPICE, ISO26262). They have a diverse team with expertise in languages like C, C++, Java, and Python, and a wide range of technologies including Windchill, Rhapsody, and Python libraries. Kmtec Ltd also supports clients with project management, technical requirements engineering, and software testing services.
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
