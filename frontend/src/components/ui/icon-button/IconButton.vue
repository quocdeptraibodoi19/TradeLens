<script setup>
import { Primitive } from "reka-ui";
import { cn } from "@/lib/utils";
import { iconButtonVariants } from ".";

const props = defineProps({
  variant: { type: null, required: false },
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
    data-slot="icon-button"
    :data-variant="variant"
    :as="as"
    :as-child="asChild"
    :class="cn(iconButtonVariants({ variant }), props.class)"
  >
    <span class="shrink-0 size-6 flex items-center justify-center">
      <slot />
    </span>
  </Primitive>
</template>
