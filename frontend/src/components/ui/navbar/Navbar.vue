<script setup>
import { RouterLink, useRoute } from 'vue-router'
import { cn } from '@/lib/utils'
import { NavbarTab } from '@/components/ui/navbar-tab'
import { Avatar } from '@/components/ui/avatar'
import logoSrc from '@/assets/logo.svg'

const props = defineProps({
  items: {
    type: Array,
    default: () => [
      { label: 'Home', to: '/home' },
      { label: 'Markets', to: '/markets' },
      { label: 'Portfolio', to: '/portfolio' },
      { label: 'Orders', to: '/orders' },
      { label: 'Alerts', to: '/alerts' },
      { label: 'AI', to: '/ai' },
    ],
  },
  userName: { type: String, default: '' },
  userSrc: { type: String, required: false },
  class: {
    type: [Boolean, null, String, Object, Array],
    required: false,
    skipCheck: true,
  },
})

const route = useRoute()

function isActive(item) {
  return route.path === item.to || (item.to !== '/' && route.path.startsWith(item.to))
}
</script>

<template>
  <header
    data-slot="navbar"
    :class="cn('bg-bg-surface w-full flex items-center justify-center px-xlarge py-small', props.class)"
  >
    <div class="flex items-center justify-between w-full max-w-[1440px]">
      <div class="flex items-end gap-[48px]">
        <img :src="logoSrc" alt="Tradelens" class="h-[33px]" />
        <nav class="flex items-center gap-medium">
          <NavbarTab
            v-for="item in items"
            :key="item.to"
            :label="item.label"
            :selected="isActive(item)"
            :as="RouterLink"
            :to="item.to"
          />
        </nav>
      </div>
      <Avatar :name="userName" :src="userSrc" />
    </div>
  </header>
</template>
