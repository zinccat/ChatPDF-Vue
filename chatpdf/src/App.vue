// App.vue
<template>
  <div class="flex flex-row space-x-4 p-4">
    <div class="flex-1">
      <UploadComponent @file-uploaded="handleFileUploaded" />
      <PdfViewerComponent v-if="pdfData" :pdfSource="pdfData" />
      <!-- <div class="flex flex-col space-y-4 mt-4"> -->
        <!-- Search and Highlight Input Groups Here -->
      <!-- </div> -->
    </div>
    <div class="w-1/3 bg-white border border-gray-300 rounded p-2">
      <div class="text-lg font-semibold mb-2">Chat</div>
      <!-- Chat Messages Display Here -->
      <div class="flex flex-col-reverse space-y-2 space-y-reverse overflow-y-auto h-96">
        <!-- Individual Chat Message Components Here -->
      </div>
      <div class="mt-2">
        <input 
          type="text" 
          placeholder="Type your message..." 
          class="w-full p-2 border border-gray-300 rounded"
        />
      </div>
    </div>
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
