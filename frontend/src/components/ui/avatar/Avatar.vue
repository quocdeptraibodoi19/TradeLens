<script setup>
import { computed } from "vue";
import { cn } from "@/lib/utils";

const props = defineProps({
  src: { type: String, required: false },
  alt: { type: String, required: false, default: "" },
  name: { type: String, required: false, default: "" },
  class: {
    type: [Boolean, null, String, Object, Array],
    required: false,
    skipCheck: true,
  },
});

const initials = computed(() => {
  const parts = props.name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return "";
  if (parts.length === 1) return parts[0][0].toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
});
</script>

<template>
  <div
    v-if="src"
    data-slot="avatar"
    :class="cn('relative shrink-0 size-12 rounded-rounded overflow-hidden flex items-center justify-center', props.class)"
  >
    <img :src="src" :alt="alt" class="size-full object-cover" />
  </div>
  <div
    v-else
    data-slot="avatar"
    :class="cn('relative shrink-0 size-12 rounded-rounded overflow-hidden flex items-center justify-center bg-display-primary-light', props.class)"
  >
    <span class="text-body-medium text-display-primary-strong select-none">
      {{ initials }}
    </span>
  </div>
</template>
