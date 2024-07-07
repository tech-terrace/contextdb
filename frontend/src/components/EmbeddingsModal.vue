<template>
    <div v-if="show" class="modal">
      <div class="modal-content">
        <h2>Get Embeddings</h2>
        <input v-model="query" placeholder="Enter your query" />
        <button @click="submitQuery">Submit</button>
        <button @click="close">Close</button>
        <div v-if="result.length > 0" class="embeddings-result">
          <h3>Results:</h3>
          <ul>
            <li v-for="(item, index) in result" :key="index">{{ item }}</li>
          </ul>
        </div>
        <div v-if="loading" class="loading-spinner"></div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, watch } from 'vue';
  import { getEmbeddings } from '../api/crud';
  
  const props = defineProps<{
    show: boolean;
    documentUrl: string;
  }>();
  
  const emit = defineEmits<{
    (e: 'close'): void;
    (e: 'submit', result: string[]): void;
  }>();
  
  const query = ref('');
  const result = ref<string[]>([]);
  const loading = ref(false);
  
  watch(() => props.show, (newValue) => {
    if (!newValue) {
      query.value = '';
      result.value = [];
      loading.value = false;
    }
  });
  
  async function submitQuery() {
    if (!query.value) return;
  
    loading.value = true;
    result.value = [];

    try {
      const results = await getEmbeddings(props.documentUrl, query.value);
      result.value = results;
      emit('submit', results);
    } catch (error) {
      console.error('Error fetching embeddings:', error);
      // You might want to show an error message to the user here
    } finally {
      loading.value = false;
    }
  }
  
  function close() {
    emit('close');
  }
  </script>
  
  <style scoped>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1001;
  }

  .modal-content {
    background-color: var(--header-bg-color);
    padding: 20px;
    border-radius: 4px;
    max-width: 500px;
    width: 100%;
  }

  .modal-content input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    font-size: 16px;
    border: 2px solid var(--link-hover-bg-color);
    background-color: #222;
    color: var(--text-active-color);
    border-radius: 4px;
    box-sizing: border-box;
  }

  .modal-content button {
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
    background-color: var(--link-hover-bg-color);
    color: var(--text-active-color);
    margin-right: 10px;
  }

  .modal-content button:hover {
    background-color: var(--active-link-color);
  }

  .embeddings-result {
    margin-top: 20px;
    max-height: 300px;
    overflow-y: auto;
  }

  .embeddings-result ul {
    padding-left: 20px;
    list-style-type: none;
  }

  .embeddings-result li {
    margin-bottom: 10px;
    color: var(--text-active-color);
  }
  </style>