<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import { login } from '@/api'

const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await login(email.value, password.value)
    router.push('/home')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-bg-canvas flex items-center justify-center">
    <div class="w-full max-w-[400px] rounded-xsmall border border-border-default bg-bg-surface-default p-xlarge flex flex-col gap-large">

      <div class="flex flex-col gap-2xsmall">
        <h1 class="text-h2-strong text-content-neutral-strong">Welcome back</h1>
        <p class="text-body-light text-content-neutral-light">Sign in to your TradeLens account</p>
      </div>

      <form class="flex flex-col gap-medium" @submit.prevent="handleLogin">

        <div class="flex flex-col gap-2xsmall">
          <label class="text-body-small-medium text-content-neutral-strong">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="you@example.com"
            required
            class="h-10 rounded-2xsmall border border-border-default bg-bg-canvas px-small text-body-medium text-content-neutral-strong placeholder:text-content-placeholder focus:outline-none focus:border-border-neutral-strong-default"
          />
        </div>

        <div class="flex flex-col gap-2xsmall">
          <label class="text-body-small-medium text-content-neutral-strong">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            required
            class="h-10 rounded-2xsmall border border-border-default bg-bg-canvas px-small text-body-medium text-content-neutral-strong placeholder:text-content-placeholder focus:outline-none focus:border-border-neutral-strong-default"
          />
        </div>

        <p v-if="error" class="text-body-small-light text-content-negative">{{ error }}</p>

        <Button type="submit" variant="accent" class="w-full" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign in' }}
        </Button>

      </form>

      <p class="text-body-small-light text-content-neutral-light text-center">
        Don't have an account?
        <router-link to="/register" class="text-body-small-medium text-content-neutral-strong hover:underline">
          Register
        </router-link>
      </p>

    </div>
  </div>
</template>
