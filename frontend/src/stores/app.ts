import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {
  const frameworkId = ref(0);
  const frameworkName = ref('');
  const frameworkDescription = ref('');

  return { frameworkId, frameworkName, frameworkDescription }
})
