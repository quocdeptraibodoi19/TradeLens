<script setup>
import { cn } from "@/lib/utils";

const props = defineProps({
  class: {
    type: [Boolean, null, String, Object, Array],
    required: false,
    skipCheck: true,
  },
});
</script>

<template>
  <td
    data-slot="table-cell"
    :class="
      cn(
        'border-b border-border-neutral-light-default',
        'px-small h-[56px]',
        'group-hover:bg-bg-fill-neutral-flat-hover transition-colors',
        props.class,
      )
    "
  >
    <slot />
  </td>
</template>
