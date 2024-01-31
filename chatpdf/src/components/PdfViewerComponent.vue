// PdfViewerComponent.vue
/* eslint-disable */
<template>
  <div v-if="pdfSource" ref="pdfViewerRef">
    <VuePdfEmbed annotation-layer text-layer :source="pdfSource" />
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

onMounted(() => {
  if (pdfViewerRef.value) {
    const intervalId = setInterval(() => {
      var textLayers = pdfViewerRef.value.querySelectorAll('.textLayer');
      
      if (textLayers.length > 0) {
        clearInterval(intervalId); // Stop polling
        textLayers.forEach(layer => {
          if (layer) {
            highlightLayer(layer);
          }
        });
      }
    }, 500); // Check every 500ms
  }
});

/* eslint-disable */
function highlightLayer(layer) {
  var query = "the";
  var re = new RegExp(query, "gi");
  var matches = layer.textContent.match(re);
  if (matches) {
    layer.innerHTML = layer.innerHTML.replace(re, function(match) {
      return "<span class='highlight'>" + match + "</span>";
    });
  }
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