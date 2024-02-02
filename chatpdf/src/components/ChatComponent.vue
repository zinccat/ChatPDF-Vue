<template>
    <div class="flex-1 overflow-y-auto p-4" style="scrollbar-width: thin; scrollbar-color: #60a5fa #e5e7eb;">
      <div v-for="(message, index) in messages" :key="index" class="chat-message mb-2">
        <div :class="{ 'text-right': message.isSentByUser, 'text-left': !message.isSentByUser }">
          <span :class="{ 'bg-blue-500': message.isSentByUser, 'bg-gray-300': !message.isSentByUser }"
                class="inline-block rounded-lg px-4 py-2 my-1 shadow" style="max-width: 75%;">
            {{ message.text }}
          </span>
        </div>
      </div>
      <div class="mt-auto">
        <div class="flex gap-2 p-2">
          <input v-model="newMessage" @keyup.enter="sendMessage" type="text" placeholder="Type your message..."
                 class="flex-1 p-4 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring focus:ring-blue-500 transition-all" />
          <button @click="clearMessages" class="px-6 py-2 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600 focus:outline-none focus:ring focus:ring-blue-500 focus:ring-opacity-50 transition duration-150 ease-in-out">
            Clear
          </button>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { performRequestWithExponentialBackoff, combineTextAndMap, pdfViewer, searchQuery, performSearch } from './utils.js'

const messages = ref([])
const newMessage = ref("")

const uploadFulltext = async () => {
    if (!pdfViewer.value) {
        console.error('PDF viewer not available')
        return
    }

    const textLayers = pdfViewer.value.querySelectorAll('.textLayer')
    // eslint-disable-next-line
    const { combinedText, textMappings } = combineTextAndMap(textLayers)

    console.log('combinedText:', combinedText)

    // Convert combinedText into a single JSON object per line (JSON Lines format)
    const jsonlString = JSON.stringify({ text: combinedText }) + '\n'
    const blob = new Blob([jsonlString], { type: 'application/json' })

    // Create FormData and append the Blob as 'file'
    const formData = new FormData()
    formData.append('file', blob, 'uploadedText.jsonl')

    // Upload combinedText in JSON Lines format to backend
    const uploadFulltextRequest = async () => {
        return axios.post('http://localhost:5005/upload', formData)
    }

    try {
        const response = await performRequestWithExponentialBackoff(uploadFulltextRequest)
        // Save fileid to localStorage
        localStorage.setItem('fileid', response.data.fileid)
    } catch (error) {
        console.error('Error uploading fulltext:', error)
        // Handle error or notify the user
        localStorage.removeItem('fileid')
    }
}

function decodeUnicodeStr(str) {
  // Wrapping the input string in double quotes makes it a valid JSON string.
  // JSON.parse will interpret the Unicode escape sequences and convert them to actual characters.
  return JSON.parse(`"${str}"`)
}

const sendMessage = async () => {
    if (!newMessage.value.trim()) return
    // if no previous messages, upload fulltext
    if (messages.value.length === 0) {
        await uploadFulltext()
    }
    const userMessage = newMessage.value.trim()
    messages.value.push({ text: userMessage, isSentByUser: true })
    newMessage.value = ""

    const sendRequest = async () => {
        return axios.post('http://localhost:5005/chat', { message: userMessage, fileid: localStorage.getItem('fileid') })
    }

    try {
        // const response = await performRequestWithExponentialBackoff(sendRequest)
        const response = await sendRequest()
        // run regex on apply to remove r"【.*?】"
        messages.value.push({ text: response.data.reply.replace(/【.*?】/g, ''), annotations: response.data.annotations, isSentByUser: false })
        for (const annotation of response.data.annotations) {
            searchQuery.value = decodeUnicodeStr(annotation)
            console.log('searchQuery:', searchQuery.value)
            performSearch()
        }
    } catch (error) {
        console.error('Error sending message:', error)
        // Handle error or notify the user
    }
}

const clearMessages = async () => {
    const clearMessagesRequest = async () => {
        return axios.post('http://localhost:5005/clear_messages')
    }
    try {
        const response = await performRequestWithExponentialBackoff(clearMessagesRequest)
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

/* Custom scrollbar styles */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #e5e7eb;
}

::-webkit-scrollbar-thumb {
  background-color: #60a5fa;
  border-radius: 20px;
  border: 3px solid #e5e7eb;
}
</style>