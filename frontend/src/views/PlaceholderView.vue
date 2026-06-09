<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<template>
  <div class="flex items-center justify-center min-h-[60vh]">
    <p class="text-h2-medium text-content-neutral-medium capitalize">{{ route.name }}</p>
  </div>
</template>
