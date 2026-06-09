import { cva } from "class-variance-authority";

export { default as IconButton } from "./IconButton.vue";

export const iconButtonVariants = cva(
  "inline-flex shrink-0 items-center justify-center select-none outline-none " +
  "rounded-action size-10 p-xsmall " +
  "transition-colors " +
  "disabled:pointer-events-none " +
  "focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-ring/50 " +
  "[&_svg]:pointer-events-none [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        primary:
          "bg-bg-fill-neutral-default hover:bg-bg-fill-neutral-hover active:bg-bg-fill-neutral-press " +
          "disabled:bg-bg-fill-disabled " +
          "text-content-inverse",
        ghost:
          "hover:bg-bg-fill-neutral-flat-hover active:bg-bg-fill-neutral-flat-press " +
          "text-content-neutral-strong disabled:text-content-disabled",
        "danger-flat":
          "hover:bg-bg-fill-negative-flat-hover active:bg-bg-fill-negative-flat-press " +
          "text-content-negative disabled:text-content-disabled",
      },
    },
    defaultVariants: { variant: "primary" },
  },
);
