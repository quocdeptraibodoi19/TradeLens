<script setup>
import { cn } from "@/lib/utils";

const props = defineProps({
  align: { type: String, default: "left" },
  class: {
    type: [Boolean, null, String, Object, Array],
    required: false,
    skipCheck: true,
  },
});
</script>

<template>
  <th
    data-slot="table-head"
    :class="
      cn(
        'border-b border-border-neutral-light-default',
        'p-small',
        'font-sans text-[length:var(--font-size-body-small)] leading-[var(--line-height-body-small)] font-medium text-content-neutral-light whitespace-nowrap',
        props.class,
      )
    "
  >
    <div
      :class="
        cn(
          'flex items-center gap-xsmall',
          align === 'right' ? 'justify-end' : 'justify-start',
        )
      "
    >
      <slot name="icon" />
      <slot />
    </div>
  </th>
</template>
