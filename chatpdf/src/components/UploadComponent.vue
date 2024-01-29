// UploadComponent.vue
<template>
  <div>
    <input type="file" @change="handleFileUpload" accept="application/pdf">
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
