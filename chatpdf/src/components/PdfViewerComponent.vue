<template>
  <div class="flex flex-col space-y-4 p-4">
    <div class="flex space-x-2">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Enter text to search" 
        class="flex-1 p-2 border border-gray-300 rounded"
      />
      <button 
        @click="performSearch" 
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Search Text
      </button>
    </div>

    <div class="flex space-x-2">
      <input 
        v-model="highlightQuery" 
        type="text" 
        placeholder="Enter text to highlight" 
        class="flex-1 p-2 border border-gray-300 rounded"
      />
      <button 
        @click="performHighlight" 
        class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
      >
        Highlight Text
      </button>
    </div>

    <div v-if="pdfSource" ref="pdfViewer" class="border border-gray-300 rounded overflow-hidden">
      <VuePdfEmbed :source="pdfSource" :key="pdfRenderKey" annotation-layer text-layer />
    </div>
  </div>
</template>

<script setup>
import VuePdfEmbed from 'vue-pdf-embed'
import 'vue-pdf-embed/dist/style/index.css'
import 'vue-pdf-embed/dist/style/annotationLayer.css'
import 'vue-pdf-embed/dist/style/textLayer.css'
import { GlobalWorkerOptions } from 'vue-pdf-embed/dist/index.essential.mjs'
import PdfWorker from 'pdfjs-dist/build/pdf.worker.js?url'
// eslint-disable-next-line no-unused-vars
import { onMounted, ref } from 'vue'
import axios from 'axios'

// PDF.js worker setup
GlobalWorkerOptions.workerSrc = PdfWorker

const pdfViewer = ref(null)
const searchQuery = ref("")
const highlightQuery = ref("")
const pdfRenderKey = ref(0)
const textMappings = ref([])

// Search text within the PDF and interact with a backend service
const performSearch = () => {
  if (!searchQuery.value) return
  const textLayers = pdfViewer.value.querySelectorAll('.textLayer')
  const { combinedText, textMappings } = combineTextAndMap(textLayers)
  axios.post('http://localhost:5005/process_text', { text: combinedText, query: searchQuery.value })
    .then(response => {
      console.log(response.data.highlight)
      const paragraphPosition = findParagraphPosition(combinedText, response.data.highlight)
      console.log(paragraphPosition)
      highlightRows(textMappings, paragraphPosition)
    })
    .catch(error => console.error('Error:', error))
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

// Identify rows that contain parts of the paragraph
function highlightRows(textMappings, paragraphPosition) {
  textMappings.value.filter(mapping =>
    mapping.start <= paragraphPosition.endPosition &&
    mapping.end >= paragraphPosition.startPosition
  ).forEach(mapping => {
    highlightNode(mapping.node)
  })
}
// eslint-disable-next-line no-unused-vars
function highlightNode(node) {
  // highlight the entire node
  node.style.backgroundColor = "yellow"
}


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

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  pdfSource: String
})
</script>

<style>
.highlight {
  background-color: yellow;
}
</style>
