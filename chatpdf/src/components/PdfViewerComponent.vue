<template>
  <div v-if="pdfSource" ref="pdfViewer" class="border border-gray-300 rounded overflow-hidden">
    <VuePdfEmbed :source="pdfSource" :key="pdfRenderKey" annotation-layer text-layer />
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import VuePdfEmbed from 'vue-pdf-embed'
import 'vue-pdf-embed/dist/style/index.css'
import 'vue-pdf-embed/dist/style/annotationLayer.css'
import 'vue-pdf-embed/dist/style/textLayer.css'
import { pdfViewer, pdfRenderKey } from './utils.js'

// eslint-disable-next-line no-unused-vars
const props = defineProps({
  pdfSource: String
})
</script>