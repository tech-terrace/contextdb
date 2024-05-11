<template>
    <div class="tool-container">
        <button @click="goBack" class="back-button">Back</button>
        <h1>{{ frameworkDetail?.name }}</h1>
        <p>{{ frameworkDetail?.description }}</p>
        <table class="versions-table">
            <thead>
                <tr>
                    <th>Version</th>
                    <th>Date</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="version in frameworkDetail?.versions" :key="version.version_number">
                    <td>{{ version.version_number }}</td>
                    <td>{{ version.release_date }}</td>
                    <td v-for="variant in version.variants" :key="variant.variant_type">
                        <div v-for="doc in variant.doc_files" :key="doc.file_name">
                            <span class="icon-link" @click="copyToClipboard(doc.file_url)" title="Copy Link"><i
                                    class="fas fa-link"></i></span>
                            <span class="icon-open-new-tab" @click="openInNewTab(doc.file_url)"
                                title="Open in New Tab"><i class="fas fa-external-link-alt"></i></span>
                            <span class="icon-copy-content" @click="copyUrlContentToClipboard(doc.file_url)"
                                title="Copy Content"><i class="fas fa-copy"></i></span>
                            <span class="icon-download" @click="downloadFile(doc.file_url)" title="Download File"><i
                                    class="fas fa-download"></i></span>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-if="loading" class="loading-spinner"></div>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { getFrameworkDetail } from '../api/crud';
import type { FrameworkDetailModel } from '../api/interfaces';
import { copyToClipboard, copyUrlContentToClipboard, openInNewTab, downloadFile } from '../utils';


const router = useRouter();
const route = useRoute();
const frameworkDetail = ref<FrameworkDetailModel | null>(null);


onMounted(async () => {
    const toolId = +route.params.toolId;
    frameworkDetail.value = await getFrameworkDetail(toolId);
});

const loading = computed(() => {
  return frameworkDetail.value === null;
});

function goBack() {
  router.back();
}
</script>

<style scoped>
.tool-container {
    width: 100%;
    max-width: 800px;
    margin: 20px auto;
    background-color: var(--header-bg-color);
    padding: 10px;
    border-radius: 4px;
    color: var(--text-active-color);
}

.versions-table {
    width: 100%;
    border-collapse: collapse;
}

.versions-table th,
.versions-table td {
    padding: 10px;
    border: 1px solid var(--link-hover-bg-color);
}

.versions-table th {
    background-color: var(--header-bg-color);
}

.icon-link i,
.icon-open-new-tab i,
.icon-download i,
.icon-copy-content i {
    cursor: pointer;
    margin-right: 10px;
}

.back-button {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  background-color: var(--header-bg-color); /* Default background */
  color: var(--text-active-color); /* Default text color */
}

.back-button:hover {
  background-color: var(--link-hover-bg-color); /* Hover background */
  color: white; /* Hover text color */
}
</style>
