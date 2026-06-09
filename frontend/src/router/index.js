import { createRouter, createWebHistory } from 'vue-router'
import OrdersView from '@/views/OrdersView.vue'
import AlertsView from '@/views/AlertsView.vue'
import SymbolsView from '@/views/SymbolsView.vue'
import PlaceholderView from '@/views/PlaceholderView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/home' },
    { path: '/home', name: 'Home', component: PlaceholderView },
    { path: '/markets', name: 'Markets', component: SymbolsView },
    { path: '/portfolio', name: 'Portfolio', component: PlaceholderView },
    { path: '/orders', name: 'Orders', component: OrdersView },
    { path: '/alerts', name: 'Alerts', component: AlertsView },
    { path: '/ai', name: 'AI', component: PlaceholderView },
  ],
})

export default router
