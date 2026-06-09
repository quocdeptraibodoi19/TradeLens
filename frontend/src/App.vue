<script setup>
import { RouterView } from 'vue-router'
import { Navbar } from '@/components/ui/navbar'
</script>

<template>
  <div class="min-h-screen bg-bg-canvas text-content-neutral-strong">
    <Navbar user-name="Le Thanh" />
    <RouterView />
  </div>
</template>
