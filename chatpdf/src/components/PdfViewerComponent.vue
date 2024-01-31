<template>
  <div v-if="pdfSource">
    <button @click="extractText">Extract Text</button>
    <div v-if="extractedText">{{ extractedText }}</div>
    <VuePdfEmbed annotation-layer text-layer :source="pdfSource" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import VuePdfEmbed from 'vue-pdf-embed';
import 'vue-pdf-embed/dist/style/index.css';
import 'vue-pdf-embed/dist/style/annotationLayer.css';
import 'vue-pdf-embed/dist/style/textLayer.css';
import { GlobalWorkerOptions } from 'vue-pdf-embed/dist/index.essential.mjs';
import PdfWorker from 'pdfjs-dist/build/pdf.worker.js?url';
import * as pdfjsLib from 'pdfjs-dist';

GlobalWorkerOptions.workerSrc = PdfWorker;

// eslint-disable-next-line
const props = defineProps({
  pdfSource: String
});

const extractedText = ref('');

const extractText = async () => {
  const loadingTask = pdfjsLib.getDocument(props.pdfSource);
  const pdfDocument = await loadingTask.promise;
  let fullText = '';

  for (let pageNumber = 1; pageNumber <= pdfDocument.numPages; pageNumber++) {
    const page = await pdfDocument.getPage(pageNumber);
    const textContent = await page.getTextContent();
    const pageText = textContent.items.map(item => item.str).join(' ');
    fullText += pageText + '\n';
    page.cleanup();
  }

  extractedText.value = fullText;
};

onMounted(() => {
  // Optionally call extractText here if you want to auto-load the text
  // extractText();
});
</script>
