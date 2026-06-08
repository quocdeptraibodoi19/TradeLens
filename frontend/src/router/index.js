import { createRouter, createWebHistory } from 'vue-router'
import OrdersView from '@/views/OrdersView.vue'
import AlertsView from '@/views/AlertsView.vue'
import SymbolsView from '@/views/SymbolsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/orders' },
    { path: '/orders', component: OrdersView },
    { path: '/alerts', component: AlertsView },
    { path: '/symbols', component: SymbolsView },
  ],
})

export default router
