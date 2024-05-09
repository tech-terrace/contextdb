<template>
  <main>
    <div>
      <div class="tags-container">
        <button v-for="tag in tags" :key="tag.id" :class="{ 'selected-tag': selectedTags.includes(tag) }"
          @click="toggleTagSelection(tag)">
          {{ tag.name }}
        </button>
      </div>
      <div class="search-container">
        <input type="text" v-model="searchTerm" placeholder="Search frameworks..." class="search-input" />
        <ul v-if="frameworks.length" class="results-list">
          <li v-for="framework in filteredFrameworks" :key="framework.id" class="result-item">
            <div class="framework-name"
              @click="clickFramework(framework)">
              {{ framework.name }} @ {{ framework.latest_version }}
            </div>
            <div class="framework-description">{{ framework.description }}</div>
            <div class="framework-icons">
              <span class="icon-link" @click="copyToClipboard(framework.latest_doc_file_url)" title="Copy Link"><i
                  class="fas fa-link"></i></span>
              <span class="icon-open-new-tab" @click="openInNewTab(framework.latest_doc_file_url)"
                title="Open in New Tab"><i class="fas fa-external-link-alt"></i></span>
              <span class="icon-copy-content" @click="copyUrlContentToClipboard(framework.latest_doc_file_url)"
                title="Copy Content"><i class="fas fa-copy"></i></span>
              <span class="icon-download" @click="downloadFile(framework.latest_doc_file_url)" title="Download File"><i
                  class="fas fa-download"></i></span>
            </div>
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
import { copyToClipboard, copyUrlContentToClipboard, openInNewTab, downloadFile } from '../utils';
import { useAppStore } from '@/stores/app';
import router from '@/router';

const searchTerm = ref('');
const frameworks = ref<FrameworkModel[]>([]);
const tags = ref<TagModel[]>([]);
const selectedTags = ref<TagModel[]>([]);


const appStore = useAppStore();

const clickFramework = (framework: FrameworkModel) => {
  appStore.frameworkId = framework.id;
  appStore.frameworkName = framework.name;
  appStore.frameworkDescription = framework.description;

  router.push({ name: 'tool', params: { toolId: framework.id } });
}

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
  max-width: 800px;
  position: relative;
  margin: 20px auto;
  background-color: var(--header-bg-color);
  padding: 10px;
  border-radius: 4px;
  box-sizing: border-box;
  /* Ensure padding is included in width */
}

.search-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 2px solid var(--link-hover-bg-color);
  background-color: #222;
  color: var(--text-active-color);
  border-radius: 4px;
  box-sizing: border-box;
  /* Include padding and border in the element's total width */
}

.results-list {
  list-style: none;
  margin: 0;
  margin-top: 5px;
  margin-left: -10px;
  padding: 0;
  background: #222;
  border: 1px solid var(--link-hover-bg-color);
  position: absolute;
  width: 100%;
  z-index: 1000;
}

.result-item {
  padding: 10px;
  border-bottom: 1px solid var(--link-hover-bg-color);
  color: var(--text-active-color);
  display: flex;
  flex-direction: column;
  align-items: start;
}

.framework-name {
  font-weight: bold;
  margin-bottom: 5px;
  color: var(--active-link-color);
  cursor: pointer;
}

.framework-description {
  color: #999;
}

.framework-icons {
  margin-top: 5px;
}

.framework-icons span {
  margin-right: 10px;
  color: var(--text-active-color);
  /* Use global variable */
}

.icon-link i,
.icon-open-new-tab i,
.icon-download i,
.icon-copy-content i {
  cursor: pointer;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 10px;
  margin-top: 10px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

button {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

button:hover {
  background-color: var(--link-hover-bg-color);
}

.selected-tag {
  background-color: var(--active-link-color);
  color: white;
  font-weight: bold;
}
</style>@/stores/app