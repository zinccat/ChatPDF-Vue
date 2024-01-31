<template>
  <button @click="extractText">Extract Text</button>
  <div v-if="extractedText">{{ extractedText }}</div>
  <div ref="pdfViewerContainer"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
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
  const loadingTask = pdfjsLib.getDocument(props.pdfSource);
  const pdfDocument = await loadingTask.promise;

  for (let pageNumber = 1; pageNumber <= pdfDocument.numPages; pageNumber++) {
    const page = await pdfDocument.getPage(pageNumber);
    const viewport = page.getViewport({ scale: 1.5 });
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

    // Now you need to add your logic to highlight 'the' on the canvas
    // This is complex as you need to parse the text items, calculate their positions, and then draw the highlights on the canvas
  }
});
</script>
