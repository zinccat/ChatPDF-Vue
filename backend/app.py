# app.py (Flask Backend)
from flask_cors import CORS, cross_origin
from flask import Flask, request, session, jsonify
from flask_session import Session
import uuid

app = Flask(__name__)
# Configure the Secret Key and Flask-Session
app.config["SECRET_KEY"] = "your-secret-key"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)

@cross_origin()
@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.json
    pdf_text = data['text']
    query = data['query']
    response = jsonify({"highlight": query})
    return response

@cross_origin()
@app.route('/chat', methods=['POST'])
def chat():
    if 'session_id' not in session:
        # Assign a unique session ID if not already assigned
        session['session_id'] = str(uuid.uuid4())

    user_message = request.json.get('message')

    if 'messages' not in session:
        session['messages'] = []

    # Save user's message to session
    session['messages'].append({'text': user_message, 'isSentByUser': True, 'session_id': session['session_id']})

    # Process the message to generate a response
    response = process_message(user_message)

    # Save bot's response to session
    session['messages'].append({'text': response, 'isSentByUser': False, 'session_id': session['session_id']})
    
    reply = jsonify({'reply': response, 'session_id': session['session_id']})
    session["messages"].append({'text': response, 'isSentByUser': False, 'session_id': session['session_id']})

    return reply

def process_message(message):
    # Placeholder for message processing logic
    return f"Echo: {message}"

@cross_origin()
@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    if 'messages' in session:
        session["session_id"] = str(uuid.uuid4()) # Generate a new session ID
        session['messages'] = []
    return jsonify({'status': 'success', 'message': 'Messages cleared'})

if __name__ == '__main__':
    app.run(debug=True, port=5005)
