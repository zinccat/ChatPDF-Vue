<template>
  <div class="flex justify-start items-center h-16 bg-gray-100 rounded-lg border-2 border-dashed border-gray-300">
    <input 
      type="file" 
      @change="handleFileUpload" 
      accept="application/pdf" 
      class="w-full h-full opacity-0 cursor-pointer"
    >
    <div class="text-gray-500 pl-4">Click or drag a PDF file here to upload</div>
  </div>
</template>

<script setup>
// import axios from 'axios';

// Emits (you might not need this anymore if the backend directly handles the file)
const emit = defineEmits(['file-uploaded'])

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => {
      emit('file-uploaded', reader.result)
    }
    // const formData = new FormData();
    // formData.append('file', file);
    
    // // Update the URL to your Flask endpoint
    // axios.post('http://localhost:5005/upload', formData, {
    //   headers: {
    //     'Content-Type': 'multipart/form-data'
    //   }
    // })
    // .then(response => {
    //   console.log(response.data);
    //   // Handle success, you can emit an event if needed
    //   // emit('file-uploaded', response.data);
    //   // save fileid to localstorage
    //   localStorage.setItem('fileid', response.data.fileid);
    // })
    // .catch(error => {
    //   console.error(error);
    //   // Handle error
    //   localStorage.removeItem('fileid');
    // });
  }
}
</script>
