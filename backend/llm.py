import os
import time
import base64
import re
import json

import openai
from openai.types.beta.threads import MessageContentImageFile
# from tools import TOOL_MAP
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)
assistant_id = os.environ.get("ASSISTANT_ID")
instructions = os.environ.get("RUN_INSTRUCTIONS", "")
assistant_title = os.environ.get("ASSISTANT_TITLE", "Assistants API UI")
enabled_file_upload_message = os.environ.get("ENABLED_FILE_UPLOAD_MESSAGE", "Upload a file")


def create_thread(content, file_id):
    messages = [
        {
            "role": "user",
            "content": content,
        }
    ]
    messages[0].update({"file_ids": [file_id]})
    thread = client.beta.threads.create(messages=messages)
    return thread


def create_message(thread, content, file_id):
    file_ids = []
    if file_id is not None:
        file_ids.append(file_id)
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=content, file_ids=file_ids
    )


def create_run(thread):
    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=assistant_id, instructions=instructions
    )
    return run


def create_file_link(file_name, file_id):
    content = client.files.content(file_id)
    content_type = content.response.headers["content-type"]
    b64 = base64.b64encode(content.text.encode(content.encoding)).decode()
    link_tag = f'<a href="data:{content_type};base64,{b64}" download="{file_name}">Download Link</a>'
    return link_tag

def get_message_and_citations(messages):
    messages_text = []
    citations = []
    for message in messages:
        message_text = ""
        if not isinstance(message, MessageContentImageFile):
            message_text = message.content[0].text
            annotations = message_text.annotations
        else:
            image_file = client.files.retrieve(message.file_id)
            messages_text.append(
                f"Click <here> to download {image_file.filename}"
            )
        for index, annotation in enumerate(annotations):
            message_text.value = message_text.value.replace(
                annotation.text, f" [{index}]"
            )

            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(
                    f"[{index}] {file_citation.quote} from {cited_file.filename}"
                )
            elif file_path := getattr(annotation, "file_path", None):
                link_tag = create_file_link(
                    annotation.text.split("/")[-1], file_path.file_id
                )
                message_text.value = re.sub(
                    r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", link_tag, message_text.value
                )

        messages_text.append(message_text.value)
        break
    return messages_text, citations

def get_message_value_list(messages):
    messages_value_list = []
    for message in messages:
        message_content = ""
        if not isinstance(message, MessageContentImageFile):
            message_content = message.content[0].text
            annotations = message_content.annotations
        else:
            image_file = client.files.retrieve(message.file_id)
            messages_value_list.append(
                f"Click <here> to download {image_file.filename}"
            )
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f" [{index}]"
            )

            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(
                    f"[{index}] {file_citation.quote} from {cited_file.filename}"
                )
            elif file_path := getattr(annotation, "file_path", None):
                link_tag = create_file_link(
                    annotation.text.split("/")[-1], file_path.file_id
                )
                message_content.value = re.sub(
                    r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", link_tag, message_content.value
                )

        message_content.value += "\n" + "\n".join(citations)
        messages_value_list.append(message_content.value)
        return messages_value_list


def get_message_list(thread, run):
    completed = False
    while not completed:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        if run.status == "completed":
            completed = True
        elif run.status == "failed":
            break
        else:
            time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    return get_message_value_list(messages)


def handle_uploaded_file(uploaded_file):
    file = client.files.create(file=uploaded_file, purpose="assistants")
    return file