<template>
  <div class="flex flex-col space-y-4 p-4">
    <div class="flex space-x-4">
      <div class="w-2/3">
        <UploadComponent @file-uploaded="handleFileUploaded" />
        <PdfViewerComponent v-if="pdfData" :pdfSource="pdfData" />
      </div>
      <div class="w-1/3">
        <SearchComponent />
        <HighlightComponent />
      </div>
    </div>
  </div>
</template>

<script setup>
import UploadComponent from './components/UploadComponent.vue'
import SearchComponent from './components/SearchComponent.vue'
import HighlightComponent from './components/HighlightComponent.vue'
import PdfViewerComponent from './components/PdfViewerComponent.vue'
import { ref } from 'vue'

const pdfData = ref(null)

const handleFileUploaded = (data) => {
  pdfData.value = data
}
</script>
