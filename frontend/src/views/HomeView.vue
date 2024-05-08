<template>
  <main>
    <div>
      <div class="tags-container">
        <button v-for="tag in tags" :key="tag.id" :class="{'selected-tag': selectedTags.includes(tag)}" @click="toggleTagSelection(tag)">
          {{ tag.name }}
        </button>
      </div>
    <div class="search-container">
      <input type="text" v-model="searchTerm" placeholder="Search frameworks..." class="search-input"/>
      <ul v-if="frameworks.length" class="results-list">
        <li v-for="framework in filteredFrameworks" :key="framework.id" class="result-item">
          <div class="framework-name">{{ framework.name }}</div>
          <div class="framework-description">{{ framework.description }}</div>
          <div class="framework-version">Latest Version: {{ framework.latest_version }}</div>
          <a :href="framework.latest_doc_file_url" target="_blank" v-if="framework.latest_doc_file_url" class="doc-link-button">Documentation</a>
          <button @click="copyToClipboard(framework.latest_doc_file_url)" v-if="framework.latest_doc_file_url">Copy Link</button>
        </li>
      </ul>
    </div>
  </div>

  </main>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { searchFrameworks, listTags } from '../api/crud';
import type { FrameworkModel, TagModel } from '../api/interfaces';

const searchTerm = ref('');
const frameworks = ref<FrameworkModel[]>([]);
const tags = ref<TagModel[]>([]);
const selectedTags = ref<TagModel[]>([]);

const fetchFrameworks = async () => {
  try {
    frameworks.value = await searchFrameworks();
  } catch (error) {
    console.error('Error fetching frameworks:', error);
  }
};

const fetchTags = async () => {
  try {
    tags.value = await listTags();
  } catch (error) {
    console.error('Error fetching tags:', error);
  }
};

const toggleTagSelection = (tag: TagModel) => {
  const index = selectedTags.value.findIndex(t => t.id === tag.id);
  if (index === -1) {
    selectedTags.value.push(tag);
  } else {
    selectedTags.value.splice(index, 1);
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

const filteredFrameworks = computed(() => {
  let filtered = frameworks.value;
  if (searchTerm.value) {
    filtered = filtered.filter(f => f.name.toLowerCase().includes(searchTerm.value.toLowerCase()));
  }
  selectedTags.value.forEach(tag => {
    filtered = filtered.filter(f => f.tags.some(t => t.id === tag.id));
  });
  return filtered;
});


fetchTags();
fetchFrameworks();
</script>

<style scoped>
.search-container {
  width: 100%;
  max-width: 600px;
  position: relative;
  margin: 0 auto; /* Center the search box horizontally */
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

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 20px;
  max-width: 600px; /* Match the search container width */
  margin-left: auto; /* Center align the container */
  margin-right: auto; /* Center align the container */
}

.selected-tag {
  background-color: #007BFF;
  color: white;
}
</style>