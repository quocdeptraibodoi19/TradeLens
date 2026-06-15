import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSymbolsStore = defineStore('symbols', () => {
  const symbols = ref([])
  return { symbols }
})
