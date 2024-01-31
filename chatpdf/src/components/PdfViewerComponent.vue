<template>
  <div>
    <input v-model="searchQuery" type="text" placeholder="Enter text to search" />
    <button @click="searchText">Search Text</button>
    <input v-model="highlightQuery" type="text" placeholder="Enter text to highlight" />
    <button @click="highlightText">Highlight Text</button>
    <div v-if="pdfSource" ref="pdfViewerRef">
      <VuePdfEmbed annotation-layer text-layer :source="pdfSource" :key="pdfReloadKey" />
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

GlobalWorkerOptions.workerSrc = PdfWorker

import { onMounted, ref } from 'vue';

const pdfViewerRef = ref(null);
const searchQuery = ref("");
const highlightQuery = ref("");
const pdfReloadKey = ref(0);
const rowMappings = ref([]);

const axios = require('axios');

function searchText() {
  if (!searchQuery.value) return; // Don't search if query is empty
  // pdfReloadKey.value++; // Increment key to force re-render of VuePdfEmbed
  // Concatenate text from all text layers
  const textLayers = pdfViewerRef.value.querySelectorAll('.textLayer');
  const { concatenatedText, rowMappings } = concatenateTextAndMapRows(textLayers);
  console.log(concatenatedText);
  console.log(rowMappings);
  // Send concatenated text to Flask backend
  axios.post('http://localhost:5000/process_text', { text: concatenatedText, query: searchQuery.value })
    .then(response => {
      const paragraph = response.data.highlight;
      const paragraphPosition = findParagraphPosition(concatenatedText, paragraph);
      console.log(paragraphPosition);
      const rowsToHighlight = identifyRowsForHighlighting(rowMappings, paragraphPosition);
      console.log(rowsToHighlight);
      highlightRows(rowsToHighlight);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Concatenate text from rows and create a mapping for each row
function concatenateTextAndMapRows(textLayers) {
  let concatenatedText = '';
  rowMappings.value = [];
  // eslint-disable-next-line
  textLayers.forEach((layer, index) => {
    // change granularity to line
    Array.from(layer.childNodes).forEach(node => {
      if (node.nodeType === Node.ELEMENT_NODE) {
        const layerText = getNodeText(node).trim() + ' ';
        const start = concatenatedText.length;
        concatenatedText += layerText;
        rowMappings.value.push({ start, end: start + layerText.length - 1, node });
      }
    });
  });
  return { concatenatedText, rowMappings };
}

function getNodeText(node) {
  if (node.nodeType === Node.TEXT_NODE) {
    return node.nodeValue;
  } else if (node.nodeType === Node.ELEMENT_NODE) {
    return Array.from(node.childNodes).map(getNodeText).join(' ');
  }
}

// Find the start and end positions of the paragraph in the concatenated text
function findParagraphPosition(concatenatedText, paragraph) {
  const startPosition = concatenatedText.indexOf(paragraph);
  return { startPosition, endPosition: startPosition + paragraph.length - 1 };
}

// Identify rows that contain parts of the paragraph
function identifyRowsForHighlighting(rowMappings, paragraphPosition) {
  return rowMappings.value.filter(mapping =>
    mapping.start <= paragraphPosition.endPosition &&
    mapping.end >= paragraphPosition.startPosition
  );
}

// Highlight the identified rows
function highlightRows(rowsToHighlight) {
  rowsToHighlight.forEach(mapping => {
    highlightNode(mapping.node)
  });
}

function highlightNode(node) {
  // highlight the entire node
  node.style.backgroundColor = "yellow";
}

onMounted(() => {
  // get full text of pdf
  // var text = "";
  // var intervalId = setInterval(() => {
  //   var textLayers = pdfViewerRef.value.querySelectorAll('.textLayer');
  //   if (textLayers.length > 0) {
  //     clearInterval(intervalId); // Stop polling
  //     textLayers.forEach(layer => {
  //       if (layer) {
  //         text += getText(layer);
  //       }
  //     });
  //     // console.log(text);
  //   }
  // }, 500); // Check every 500ms
});

function highlightText() {
  if (!highlightQuery.value) return; // Don't highlight if query is empty
  pdfReloadKey.value++; // Increment key to force re-render of VuePdfEmbed
  // continue after re-render
  setTimeout(() => {
    var textLayers = pdfViewerRef.value.querySelectorAll('.textLayer');
    textLayers.forEach(layer => {
      highlightWordInLayer(layer);
    });
  }, 100);
}
function highlightWordInLayer(layer) {
  if (!highlightQuery.value) return; // Don't highlight if query is empty
  var re = new RegExp(`\\b${highlightQuery.value}\\b`, "gi");

  // Function to recursively highlight text nodes
  function highlightTextNodes(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      var text = node.nodeValue;
      var matches = text.match(re);
      if (matches) {
        var highlightedText = text.replace(re, "<span class='highlight'>$&</span>");
        var fragment = document.createRange().createContextualFragment(highlightedText);
        node.replaceWith(fragment);
      }
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      Array.from(node.childNodes).forEach(highlightTextNodes);
    }
  }

  highlightTextNodes(layer);
}


// eslint-disable-next-line
const props = defineProps({
  pdfSource: String
})
</script>

<style>
.highlight {
  background-color: yellow;
}
</style>
