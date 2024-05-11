import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {
  const frameworkId = ref(0);

  return { frameworkId}
})
