<script setup>
import { Navbar } from '@/components/ui/navbar'

defineProps({
  userName: { type: String, default: '' },
  userSrc: { type: String, required: false },
})
</script>

<template>
  <div class="min-h-screen bg-bg-canvas flex flex-col text-content-neutral-strong">
    <Navbar :user-name="userName" :user-src="userSrc" />
    <main class="flex flex-1 flex-col items-center p-4xlarge">
      <div class="w-full max-w-[1440px]">
        <slot />
      </div>
    </main>
  </div>
</template>
