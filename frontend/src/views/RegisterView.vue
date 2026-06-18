<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import { register } from '@/api'

const router = useRouter()

const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await register(firstName.value, lastName.value, email.value, password.value)
    router.push('/login')
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
        <h1 class="text-h2-strong text-content-neutral-strong">Create account</h1>
        <p class="text-body-light text-content-neutral-light">Start tracking your trades with TradeLens</p>
      </div>

      <form class="flex flex-col gap-medium" @submit.prevent="handleRegister">

        <div class="flex gap-small">
          <div class="flex flex-col gap-2xsmall flex-1">
            <label class="text-body-small-medium text-content-neutral-strong">First name</label>
            <input
              v-model="firstName"
              type="text"
              placeholder="John"
              required
              class="h-10 rounded-2xsmall border border-border-default bg-bg-canvas px-small text-body-medium text-content-neutral-strong placeholder:text-content-placeholder focus:outline-none focus:border-border-neutral-strong-default"
            />
          </div>
          <div class="flex flex-col gap-2xsmall flex-1">
            <label class="text-body-small-medium text-content-neutral-strong">Last name</label>
            <input
              v-model="lastName"
              type="text"
              placeholder="Doe"
              required
              class="h-10 rounded-2xsmall border border-border-default bg-bg-canvas px-small text-body-medium text-content-neutral-strong placeholder:text-content-placeholder focus:outline-none focus:border-border-neutral-strong-default"
            />
          </div>
        </div>

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
          {{ loading ? 'Creating account...' : 'Create account' }}
        </Button>

      </form>

      <p class="text-body-small-light text-content-neutral-light text-center">
        Already have an account?
        <router-link to="/login" class="text-body-small-medium text-content-neutral-strong hover:underline">
          Sign in
        </router-link>
      </p>

    </div>
  </div>
</template>
