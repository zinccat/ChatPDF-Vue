// UploadComponent.vue
<template>
  <div class="flex justify-center items-center h-16 bg-gray-100 rounded-lg border-2 border-dashed border-gray-300">
    <input 
      type="file" 
      @change="handleFileUpload" 
      accept="application/pdf" 
      class="w-full h-full opacity-0 cursor-pointer"
    >
    <div class="text-gray-500">Click or drag a PDF file here to upload</div>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue'

// Emits
const emit = defineEmits(['file-uploaded'])

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => {
      emit('file-uploaded', reader.result)
    }
  }
}
</script>
