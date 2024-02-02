<template>
  <div class="flex flex-col space-y-4 p-4">
    <div class="flex space-x-4">
      <div class="w-2/3">
        <div class="pdf-viewer-container custom-scroll" style="height: 95vh;">
          <UploadComponent v-if="!pdfData" @file-uploaded="handleFileUploaded" />
          <PdfViewerComponent v-if="pdfData" :pdfSource="pdfData" />
        </div>
      </div>
      <div class="w-1/3">
        <UploadComponent v-if="pdfData" @file-uploaded="handleFileUploaded" />
        <div class="chat-container custom-scroll" style="height: 85vh;">
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

<style>
/* Add these styles to your stylesheet */
.custom-scroll {
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--scrollbar-thumb-color) var(--scrollbar-track-color);
}

.custom-scroll::-webkit-scrollbar {
  width: 8px;
}

.custom-scroll::-webkit-scrollbar-track {
  background: var(--scrollbar-track-color);
}

.custom-scroll::-webkit-scrollbar-thumb {
  background-color: var(--scrollbar-thumb-color);
  border-radius: 20px;
  border: 3px solid var(--scrollbar-track-color);
}
</style>