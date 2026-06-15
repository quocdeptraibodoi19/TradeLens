<script setup>
import { Primitive } from "reka-ui";
import { cn } from "@/lib/utils";
import { buttonVariants } from ".";

const props = defineProps({
  variant: { type: null, required: false },
  iconPosition: { type: String, required: false, default: "none" },
  class: {
    type: [Boolean, null, String, Object, Array],
    required: false,
    skipCheck: true,
  },
  asChild: { type: Boolean, required: false },
  as: { type: null, required: false, default: "button" },
});
</script>

<template>
  <Primitive
    data-slot="button"
    :data-variant="variant"
    :as="as"
    :as-child="asChild"
    :class="cn(buttonVariants({ variant, iconPosition }), props.class)"
  >
    <span v-if="iconPosition === 'left'" class="shrink-0 size-6 flex items-center justify-center">
      <slot name="icon" />
    </span>

    <span class="flex items-center justify-center px-2xsmall">
      <slot />
    </span>

    <span v-if="iconPosition === 'right'" class="shrink-0 size-6 flex items-center justify-center">
      <slot name="icon" />
    </span>
  </Primitive>
</template>
