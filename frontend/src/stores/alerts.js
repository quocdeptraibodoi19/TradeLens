import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAlertsStore = defineStore('alerts', () => {
  const alerts = ref([])
  return { alerts }
})
