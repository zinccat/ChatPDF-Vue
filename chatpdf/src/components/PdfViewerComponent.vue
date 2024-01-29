// PdfViewerComponent.vue
<template>
  <div v-if="pdfSource">
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

// eslint-disable-next-line
const props = defineProps({
  pdfSource: String
})
</script>
