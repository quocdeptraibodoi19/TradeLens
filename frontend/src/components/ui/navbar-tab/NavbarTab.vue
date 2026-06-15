<script setup>
import { Primitive } from "reka-ui";
import { cn } from "@/lib/utils";

const props = defineProps({
  label: { type: String, required: true },
  selected: { type: Boolean, default: false },
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
    data-slot="navbar-tab"
    :data-selected="selected"
    :as="as"
    :as-child="asChild"
    :class="cn(
      'inline-flex items-center justify-center whitespace-nowrap cursor-pointer select-none outline-none',
      'rounded-3xsmall px-small py-2xsmall',
      'transition-colors',
      'text-content-neutral-strong',
      'focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-ring/50',
      selected
        ? 'bg-bg-fill-primary-flat-selected text-body-strong'
        : 'hover:bg-bg-fill-primary-flat-hover text-body-medium',
      props.class,
    )"
  >{{ label }}</Primitive>
</template>
