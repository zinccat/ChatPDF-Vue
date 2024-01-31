# app.py (Flask Backend)
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.json
    pdf_text = data['text']
    query = data['query']

    print(query)
    
    # Process the text here as per your requirements
    # For example, find specific keywords or patterns
    # This is a placeholder for your text processing logic
    processed_text = your_text_processing_function(pdf_text)
    processed_text = "the"

    return jsonify({"highlight": query })

def your_text_processing_function(text):
    # Implement your text processing logic here
    # For demonstration, let's just return the text as is
    return text

if __name__ == '__main__':
    app.run(debug=True)
