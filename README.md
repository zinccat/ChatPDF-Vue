# ChatPDF

Chat with your PDF file using OpenAI's assistant API, with highlights for annotations retrieved from the chat.

## Installation
### Backend
In the `backend` directory, run:

```bash
pip install -r requirements.txt
```

### Frontend
In the `chatpdf` directory, run:

```bash
npm install
```

### OpenAI platform
You will need to create an account on OpenAI's platform and get an API key. You can find more information [here](https://beta.openai.com/docs/get-started/quickstart).

Then, at [here](https://platform.openai.com/assistants), create a new assistant and get the assistant's ID. Example prompt for the assistant:

```text
You are a helpful assistant. Your task is to review a file from 'data/xxxx, it is in your Files, you must generate the response based on the file.
```

Finally, fill in the `backend/.env` file with the API key and the assistant's ID.

## Usage
### Frontend
In the `backend` directory, run:

```bash
npm run serve
```

### Backend
In the `chatpdf` directory, run:

```bash
python app.py
```

### Acknowledgements
Favicon taken from https://icon-icons.com.

Part of the OpenAI's assistant API code was taken from https://github.com/ryo-ma/gpt-assistants-api-ui.

Thanks a lot to all the contributors of the above projects.