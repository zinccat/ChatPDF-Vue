# app.py (Flask Backend)
from flask_cors import CORS, cross_origin
from flask import Flask, request, session, jsonify
from flask_session import Session
import uuid
import os
from dotenv import load_dotenv
from llm import create_thread, create_message, create_run, client, handle_uploaded_file, get_message_and_citations
from logging import getLogger
import time

load_dotenv()

logger = getLogger(__name__)

app = Flask(__name__)
# Configure the Secret Key and Flask-Session
app.config["SESSION_PERMANENT"] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SESSION_TYPE"] = os.environ.get("SESSION_TYPE")
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    fileid = request.json.get('fileid')

    if 'messages' not in session:
        session['messages'] = []

    # Save user's message to session
    session['messages'].append({'text': user_message, 'isSentByUser': True, 'session_id': session['session_id']})
    
    response, annotations = get_response(user_message, fileid)

    print(annotations)

    # Save bot's response to session
    session['messages'].append({'text': response, 'isSentByUser': False, 'session_id': session['session_id']})
    
    reply = jsonify({'reply': response, 'session_id': session['session_id'], 'annotations': annotations})
    session["messages"].append({'text': response, 'annotations': annotations,
                                'isSentByUser': False, 'session_id': session['session_id']})
    return reply

def get_response(user_input, fileid):
    if "thread" not in session:
        session["thread"] = create_thread(user_input, fileid)
    else:
        create_message(session["thread"], user_input, fileid)
    run = create_run(session["thread"])
    run = client.beta.threads.runs.retrieve(
        thread_id=session["thread"].id, run_id=run.id
    )

    while run.status == "in_progress":
        logger.info("run.status: %s", run.status)
    
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=session["thread"].id, run_id=run.id
        )
        run_steps = client.beta.threads.runs.steps.list(
            thread_id=session["thread"].id, run_id=run.id
        )
        logger.info("run_steps: %s", run_steps)
    
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=session["thread"].id)
        messages_list, annotations = get_message_and_citations(messages)
        response = messages_list[-1]
        annotations = annotations
        return response, annotations
    else:
        return "Run failed"

# define a api to upload file
@cross_origin()
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file = file.read()
        file_obj = handle_uploaded_file(file)
        return jsonify({'status': 'success', 'fileid': file_obj.id})
    else:
        return jsonify({'status': 'error', 'message': 'No file found'})
    

@cross_origin()
@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    if 'messages' in session:
        session["session_id"] = str(uuid.uuid4()) # Generate a new session ID
        session['messages'] = []
    return jsonify({'status': 'success', 'message': 'Messages cleared'})

if __name__ == '__main__':
    app.run(debug=True, port=5005)
