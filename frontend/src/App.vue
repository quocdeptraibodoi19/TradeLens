<script setup>
import { RouterView } from 'vue-router'
import ScreenTemplate from '@/components/layout/ScreenTemplate.vue'
</script>

<template>
  <ScreenTemplate user-name="Le Thanh">
    <RouterView />
  </ScreenTemplate>
</template>
