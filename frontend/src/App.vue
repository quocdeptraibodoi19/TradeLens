<script setup>
import { computed, ref, watch } from 'vue'
import { RouterView, useRoute, useRouter } from 'vue-router'
import ScreenTemplate from '@/components/layout/ScreenTemplate.vue'
import { fetchMe, logout } from '@/api'

const route = useRoute()
const router = useRouter()
const me = ref(null)

const userName = computed(() => (me.value ? `${me.value.first_name} ${me.value.last_name}` : ''))

async function loadMe() {
  try {
    me.value = await fetchMe()
  } catch {
    me.value = null
  }
}

// Re-check on navigation so the name appears right after login and clears after logout.
watch(() => route.path, loadMe, { immediate: true })

async function onLogout() {
  try {
    await logout()
  } finally {
    me.value = null
    router.push('/login')
  }
}
</script>

<template>
  <ScreenTemplate :user-name="userName" @logout="onLogout">
    <RouterView />
  </ScreenTemplate>
</template>
