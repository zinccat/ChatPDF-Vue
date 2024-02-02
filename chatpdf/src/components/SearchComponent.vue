<template>
    <div class="flex space-x-2">
        <input v-model="searchQuery" type="text" placeholder="Enter text to search"
            class="flex-1 p-2 border border-gray-300 rounded" />
        <button @click="performSearch" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Search Text
        </button>
    </div>
</template>
  
<script setup>
import { performSearch, searchQuery  } from './utils.js'
</script>
  