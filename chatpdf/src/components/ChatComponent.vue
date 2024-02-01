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
import { performRequestWithExponentialBackoff } from './utils.js'

const messages = ref([])
const newMessage = ref("")

const sendMessage = async () => {
    if (!newMessage.value.trim()) return;
    const userMessage = newMessage.value.trim();
    messages.value.push({ text: userMessage, isSentByUser: true });
    newMessage.value = "";

    const sendRequest = async () => {
        return axios.post('http://localhost:5005/chat', { message: userMessage, fileid: localStorage.getItem('fileid') });
    };

    try {
        // const response = await performRequestWithExponentialBackoff(sendRequest);
        const response = await sendRequest();
        messages.value.push({ text: response.data.reply, isSentByUser: false });
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
  