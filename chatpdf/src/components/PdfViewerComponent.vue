<template>
  <button @click="extractText">Extract Text</button>
  <div v-if="extractedText">{{ extractedText }}</div>
  <div ref="pdfViewerContainer"></div>
</template>

<script setup>
import { onMounted, ref, defineProps, watchEffect } from 'vue';
import * as pdfjsLib from 'pdfjs-dist/build/pdf';
import PdfWorker from 'pdfjs-dist/build/pdf.worker.entry';

pdfjsLib.GlobalWorkerOptions.workerSrc = PdfWorker;

const props = defineProps({
  pdfSource: String
});

const pdfViewerContainer = ref(null);
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

onMounted(async () => {
  // Initially load the PDF
  // await loadPDF();

  // Watch for changes in the pdfSource prop and reload the PDF when it changes
  watchEffect(() => {
    loadPDF();
  });
});

async function loadPDF() {
  // Clear previous canvases
  pdfViewerContainer.value.innerHTML = '';

  const loadingTask = pdfjsLib.getDocument(props.pdfSource);
  const pdfDocument = await loadingTask.promise;

  for (let pageNumber = 1; pageNumber <= pdfDocument.numPages; pageNumber++) {
    const page = await pdfDocument.getPage(pageNumber);
    const viewport = page.getViewport({ scale: 1 });
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    const renderContext = {
      canvasContext: context,
      viewport: viewport
    };
    await page.render(renderContext).promise;

    pdfViewerContainer.value.appendChild(canvas);

    // Highlight the occurrences of 'the' on the canvas
    // highlightText(canvas, 'the');
  }
}
</script>
