// App.vue
<template>
  <div>
    <UploadComponent @file-uploaded="handleFileUploaded" />
    <PdfViewerComponent v-if="pdfData" :pdfSource="pdfData" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import UploadComponent from './components/UploadComponent.vue'
import PdfViewerComponent from './components/PdfViewerComponent.vue'

const pdfData = ref(null)

const handleFileUploaded = (data) => {
  pdfData.value = data
}
</script>
