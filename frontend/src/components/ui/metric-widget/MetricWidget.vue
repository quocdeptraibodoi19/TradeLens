<script setup>
import { cn } from "@/lib/utils";
import { metricWidgetVariants } from ".";

const props = defineProps({
  variant: { type: String, required: false, default: "indigo" },
  label:   { type: String, required: false, default: "Label" },
  value:   { type: String, required: false, default: "$24,810" },
  class:   { type: [Boolean, null, String, Object, Array], required: false },
});
</script>

<template>
  <div :class="cn(metricWidgetVariants({ variant }), props.class)">
    <p class="text-body-medium w-full" :class="variant === 'pink' ? 'text-content-neutral-light' : ''">
      {{ label }}
    </p>
    <p class="text-h1-strong w-full" :class="variant === 'pink' ? 'text-display-pink-on-subtle' : ''">
      {{ value }}
    </p>
  </div>
</template>
