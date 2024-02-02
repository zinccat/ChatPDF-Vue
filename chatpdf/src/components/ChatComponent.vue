<template>
    <div class="flex-1 overflow-y-auto p-2">
        <div v-for="(message, index) in messages" :key="index" class="chat-message">
            <div :class="{ 'text-right': message.isSentByUser, 'text-left': !message.isSentByUser }">
                <span :class="{ 'bg-blue-200': message.isSentByUser, 'bg-gray-200': !message.isSentByUser }"
                    class="inline-block rounded px-2 py-1 my-1">
                    {{ message.text }}
                </span>
            </div>
        </div>
        <input v-model="newMessage" @keyup.enter="sendMessage" type="text" placeholder="Type your message..."
            class="w-full p-2 border border-gray-300 rounded" />
        <button @click="clearMessages" class="clear-messages-button">
            Clear Messages
        </button>
    </div>
</template>
  
<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { performRequestWithExponentialBackoff, combineTextAndMap, pdfViewer } from './utils.js'

const messages = ref([])
const newMessage = ref("")

const uploadFulltext = async () => {
    if (!pdfViewer.value) {
        console.error('PDF viewer not available');
        return;
    }

    const textLayers = pdfViewer.value.querySelectorAll('.textLayer');
    // eslint-disable-next-line
    const { combinedText, textMappings } = combineTextAndMap(textLayers);

    // Convert combinedText into a single JSON object per line (JSON Lines format)
    const jsonlString = JSON.stringify({ text: combinedText }) + '\n';
    const blob = new Blob([jsonlString], { type: 'application/json' });

    // Create FormData and append the Blob as 'file'
    const formData = new FormData();
    formData.append('file', blob, 'uploadedText.jsonl');

    // Upload combinedText in JSON Lines format to backend
    const uploadFulltextRequest = async () => {
        return axios.post('http://localhost:5005/upload', formData);
    };

    try {
        const response = await performRequestWithExponentialBackoff(uploadFulltextRequest);
        // Save fileid to localStorage
        localStorage.setItem('fileid', response.data.fileid);
        console.log(response.data);
    } catch (error) {
        console.error('Error uploading fulltext:', error);
        // Handle error or notify the user
        localStorage.removeItem('fileid');
    }
};

const sendMessage = async () => {
    if (!newMessage.value.trim()) return;
    // if no previous messages, upload fulltext
    if (messages.value.length === 0) {
        await uploadFulltext();
    }
    const userMessage = newMessage.value.trim();
    messages.value.push({ text: userMessage, isSentByUser: true });
    newMessage.value = "";

    const sendRequest = async () => {
        return axios.post('http://localhost:5005/chat', { message: userMessage, fileid: localStorage.getItem('fileid') });
    };

    try {
        // const response = await performRequestWithExponentialBackoff(sendRequest);
        const response = await sendRequest();
        messages.value.push({ text: response.data.reply, annotations: response.data.annotations, isSentByUser: false });
    } catch (error) {
        console.error('Error sending message:', error);
        // Handle error or notify the user
    }
};

const clearMessages = async () => {
    const clearMessagesRequest = async () => {
        return axios.post('http://localhost:5005/clear_messages');
    };
    try {
        const response = await performRequestWithExponentialBackoff(clearMessagesRequest);
        if (response.data.status === 'success') {
            messages.value = []
        }
    } catch (error) {
        console.error('Error clearing messages:', error)
        // Handle error or notify the user
    }
}
</script>

<style scoped>
.chat-message {
    display: block;
    margin-bottom: 8px;
}
</style>
  