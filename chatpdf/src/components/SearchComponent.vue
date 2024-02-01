<template>
    <div class="flex space-x-2">
        <input v-model="searchQuery" type="text" placeholder="Enter text to search"
            class="flex-1 p-2 border border-gray-300 rounded" />
        <button @click="performSearch" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Search Text
        </button>
    </div>
</template>
  
<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { highlightRows } from './utils.js'
import { pdfViewer, performRequestWithExponentialBackoff } from './utils.js'
//

const searchQuery = ref("")
const textMappings = ref([])

// Search text within the PDF and interact with a backend service
const performSearch = async () => {
    if (!searchQuery.value || !pdfViewer.value) {
        console.error('Search query or PDF viewer not available')
        return
    }
    const textLayers = pdfViewer.value.querySelectorAll('.textLayer')
    const { combinedText, textMappings } = combineTextAndMap(textLayers)

    // eslint-disable-next-line no-unused-vars
    const sendRequest = async () => {
        return axios.post('http://localhost:5005/process_text', { text: combinedText, query: searchQuery.value })
    }
    // axios.post('http://localhost:5005/process_text', { text: combinedText, query: searchQuery.value })
    //     .then(response => {
    //         console.log(response.data.highlight)
    //         const paragraphPosition = findParagraphPosition(combinedText, response.data.highlight)
    //         console.log(paragraphPosition)
    //         highlightRows(textMappings, paragraphPosition)
    //     })
    //     .catch(error => console.error('Error:', error))
    try {
        console.log('sendRequest')
        const response = await performRequestWithExponentialBackoff(sendRequest)
        console.log(response.data.highlight)
        const paragraphPosition = findParagraphPosition(combinedText, response.data.highlight)
        console.log(paragraphPosition)
        highlightRows(textMappings, paragraphPosition)
    } catch (error) {
        console.error('Error:', error)
    }
}

// Combine text from PDF text layers and map each text's position
const combineTextAndMap = (textLayers) => {
    let combinedText = ''
    textMappings.value = []
    textLayers.forEach((layer) => {
        Array.from(layer.childNodes).forEach(node => {
            if (node.nodeType === Node.ELEMENT_NODE) {
                const nodeText = getNodeText(node).trim() + ' '
                const start = combinedText.length
                combinedText += nodeText
                textMappings.value.push({ start, end: start + nodeText.length - 1, node })
            }
        })
    })
    return { combinedText, textMappings }
}

const getNodeText = (node) => node.nodeType === Node.TEXT_NODE ? node.nodeValue :
    node.nodeType === Node.ELEMENT_NODE ? Array.from(node.childNodes).map(getNodeText).join(' ') : ''

// Process highlight response from backend
function findParagraphPosition(combinedText, paragraph) {
    const startPosition = combinedText.indexOf(paragraph)
    return { startPosition, endPosition: startPosition + paragraph.length - 1 }
}
</script>
  