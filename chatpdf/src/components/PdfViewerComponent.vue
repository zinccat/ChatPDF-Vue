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

const axios = require('axios');

function searchText() {
  if (!searchQuery.value) return; // Don't search if query is empty
  // pdfReloadKey.value++; // Increment key to force re-render of VuePdfEmbed

  // Fetch full text of the PDF
  var fullText = "";
  var textLayers = pdfViewerRef.value.querySelectorAll('.textLayer');
  textLayers.forEach(layer => {
    fullText += getText(layer) + " ";
  });

  // Send full text to Flask backend for processing
  axios.post('http://localhost:5000/process_text', { text: fullText })
    .then(response => {
      const highlightString = response.data.highlight;
      highlightQuery.value = highlightString; // Update the highlight query with response
      highlightText(); // Highlight the text
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

onMounted(() => {
  // get full text of pdf
  var text = "";
  var intervalId = setInterval(() => {
    var textLayers = pdfViewerRef.value.querySelectorAll('.textLayer');
    if (textLayers.length > 0) {
      clearInterval(intervalId); // Stop polling
      textLayers.forEach(layer => {
        if (layer) {
          text += getText(layer);
        }
      });
      console.log(text);
    }
  }, 500); // Check every 500ms
});

function getText(layer) {
  var text = "";
  // remove preceding and trailing whitespaces
  Array.from(layer.childNodes).forEach(node => {
    if (node.nodeType === Node.TEXT_NODE) {
      text += node.nodeValue.trim();
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      text += getText(node);
    }
    text += " ";
  });
  return text;
}

function highlightText() {
  if (!highlightQuery.value) return; // Don't highlight if query is empty
  pdfReloadKey.value++; // Increment key to force re-render of VuePdfEmbed
  // continue after re-render
  setTimeout(() => {
    var textLayers = pdfViewerRef.value.querySelectorAll('.textLayer');
    textLayers.forEach(layer => {
      highlightLayer(layer);
    });
  }, 100);
}

function highlightLayer(layer) {
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
