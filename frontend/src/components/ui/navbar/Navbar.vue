<script setup>
import { ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { onClickOutside, onKeyStroke } from '@vueuse/core'
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

const emit = defineEmits(['logout'])

const route = useRoute()
const menuOpen = ref(false)
const menuRef = ref(null)

onClickOutside(menuRef, () => (menuOpen.value = false))
onKeyStroke('Escape', () => (menuOpen.value = false))

function onLogout() {
  menuOpen.value = false
  emit('logout')
}

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
      <div ref="menuRef" class="relative">
        <button
          type="button"
          class="rounded-rounded outline-none focus-visible:ring-2 focus-visible:ring-display-indigo-default transition-transform hover:scale-105"
          aria-haspopup="menu"
          :aria-expanded="menuOpen"
          @click="menuOpen = !menuOpen"
        >
          <Avatar :name="userName" :src="userSrc" />
        </button>
        <Transition
          enter-active-class="transition duration-150 ease-out"
          enter-from-class="opacity-0 -translate-y-1 scale-95"
          leave-active-class="transition duration-100 ease-in"
          leave-to-class="opacity-0 -translate-y-1 scale-95"
        >
          <div
            v-if="menuOpen"
            role="menu"
            class="absolute right-0 top-full mt-small z-50 w-56 origin-top-right rounded-xsmall border border-border-default bg-bg-surface p-xsmall shadow-lg"
          >
            <div v-if="userName" class="px-small py-xsmall">
              <p class="text-body-small-strong">{{ userName }}</p>
              <p class="text-caption-medium text-content-neutral-light">Signed in</p>
            </div>
            <hr v-if="userName" class="border-border-default my-xsmall" />
            <button
              type="button"
              role="menuitem"
              class="flex w-full items-center gap-small rounded-3xsmall px-small py-xsmall text-left text-body-small-medium text-content-negative hover:bg-display-red-light"
              @click="onLogout"
            >
              <font-awesome-icon icon="fa-solid fa-arrow-right-from-bracket" />
              Log out
            </button>
          </div>
        </Transition>
      </div>
    </div>
  </header>
</template>
