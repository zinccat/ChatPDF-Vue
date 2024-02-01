/* eslint-disable */
<template>
    <div class="flex space-x-2">
        <input v-model="highlightQuery" type="text" placeholder="Enter text to highlight"
            class="flex-1 p-2 border border-gray-300 rounded" />
        <button @click="performHighlight" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
            Highlight Text
        </button>
    </div>
</template>
  
<script setup>
import { ref } from 'vue'
import { pdfRenderKey, pdfViewer } from './utils.js'

const highlightQuery = ref("")

// Perform highlight based on user input
const performHighlight = () => {
    if (!highlightQuery.value) return
    pdfRenderKey.value++
    setTimeout(() => {
        const textLayers = pdfViewer.value.querySelectorAll('.textLayer')
        textLayers.forEach(layer => highlightLayerText(layer, highlightQuery.value))
    }, 100)
}

// Highlight specific text within a layer
const highlightLayerText = (layer, query) => {
    const regex = new RegExp(`\\b${query}\\b`, "gi")
    const highlightNodeText = (node) => {
        if (node.nodeType === Node.TEXT_NODE && regex.test(node.nodeValue)) {
            const highlightedHTML = node.nodeValue.replace(regex, "<span class='highlight'>$&</span>")
            const fragment = document.createRange().createContextualFragment(highlightedHTML)
            node.replaceWith(fragment)
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            Array.from(node.childNodes).forEach(highlightNodeText)
        }
    }
    highlightNodeText(layer)
}
</script>

<!-- export { highlightRows } -->