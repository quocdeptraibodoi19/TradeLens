import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useOrdersStore = defineStore('orders', () => {
  const orders = ref([])
  return { orders }
})
