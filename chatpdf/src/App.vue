<template>
  <div class="flex flex-col space-y-4 p-4">
    <div class="flex space-x-4">
      <div class="w-2/3">
        <div class="pdf-viewer-container" style="height: 900px; overflow-y: auto;">
          <UploadComponent v-if="!pdfData" @file-uploaded="handleFileUploaded" />
          <PdfViewerComponent v-if="pdfData" :pdfSource="pdfData" />
        </div>
      </div>
      <div class="w-1/3">
        <UploadComponent v-if="pdfData" @file-uploaded="handleFileUploaded" />
        <!-- <SearchComponent v-if="pdfData" :pdfData="pdfData" /> -->
        <!-- <HighlightComponent /> -->
        <div class="chat-container" style="overflow-y: auto;">
          <ChatComponent v-if="pdfData" />
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import UploadComponent from './components/UploadComponent.vue'
// import SearchComponent from './components/SearchComponent.vue'
// import HighlightComponent from './components/HighlightComponent.vue'
import PdfViewerComponent from './components/PdfViewerComponent.vue'
import ChatComponent from './components/ChatComponent.vue'
import { ref } from 'vue'

const pdfData = ref(null)

const handleFileUploaded = (data) => {
  pdfData.value = data
}
</script>
