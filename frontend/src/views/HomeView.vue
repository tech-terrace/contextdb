<template>
  <main>
    <div class="search-container">
      <input type="text" v-model="searchTerm" placeholder="Search frameworks..." class="search-input"/>
      <ul v-if="frameworks.length" class="results-list">
        <li v-for="framework in frameworks" :key="framework.id" class="result-item">
          <div class="framework-name">{{ framework.name }}</div>
          <div class="framework-description">{{ framework.description }}</div>
          <div class="framework-version">Latest Version: {{ framework.latest_version }}</div>
          <a :href="framework.latest_doc_file_url" target="_blank" v-if="framework.latest_doc_file_url" class="doc-link-button">Documentation</a>
          <button @click="copyToClipboard(framework.latest_doc_file_url)" v-if="framework.latest_doc_file_url">Copy Link</button>
        </li>
      </ul>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { searchFrameworks } from '../api/crud';
import type { FrameworkModel } from '../api/interfaces';

const searchTerm = ref('');
const frameworks = ref<FrameworkModel[]>([]);
const fetchFrameworks = async () => {
  try {
    frameworks.value = await searchFrameworks(searchTerm.value);
  } catch (error) {
    console.error('Error fetching frameworks:', error);
  }
};

const copyToClipboard = async (url: string) => {
  try {
    await navigator.clipboard.writeText(url);
    alert('Link copied to clipboard!');
  } catch (error) {
    console.error('Failed to copy:', error);
  }
};


watch(searchTerm, fetchFrameworks, { immediate: true });
</script>

<style scoped>
.search-container {
  width: 100%;
  max-width: 600px;
  position: relative;
  margin: 20px auto;
}

.search-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.results-list {
  list-style: none;
  margin: 0;
  padding: 0;
  background: white;
  border: 1px solid #ccc;
  border-top: none;
  border-radius: 0 0 4px 4px;
  position: absolute;
  width: 100%;
  z-index: 1000;
}

.result-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
  display: flex;
  flex-direction: column;
  align-items: start;
}

.result-item:last-child {
  border-bottom: none;
}

.framework-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.framework-description {
  color: #666;
}

.doc-link-button {
  margin-right: 10px;
  padding: 5px 10px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
}
</style>