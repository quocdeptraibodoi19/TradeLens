<script setup>
import { Primitive } from "reka-ui";
import { cn } from "@/lib/utils";
import { badgeVariants } from ".";

const props = defineProps({
  variant: { type: null, required: false },
  as:      { type: null, required: false, default: "span" },
  class: {
    type: [Boolean, null, String, Object, Array],
    required: false,
    skipCheck: true,
  },
});
</script>

<template>
  <Primitive
    data-slot="badge"
    :data-variant="variant"
    :as="as"
    :class="cn(badgeVariants({ variant }), props.class)"
  >
    <slot />
  </Primitive>
</template>
