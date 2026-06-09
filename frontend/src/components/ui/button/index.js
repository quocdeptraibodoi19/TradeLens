import { cva } from "class-variance-authority";

export { default as Button } from "./Button.vue";

export const buttonVariants = cva(
  "inline-flex shrink-0 items-center justify-center whitespace-nowrap select-none outline-none " +
  "rounded-action " +
  "text-button leading-button font-semibold font-sans " +
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
          "text-content-inverse " +
          "px-medium py-xsmall",
        accent:
          "bg-bg-fill-primary-default hover:bg-bg-fill-primary-hover active:bg-bg-fill-primary-press " +
          "disabled:bg-bg-fill-disabled " +
          "text-content-neutral-strong active:text-content-inverse disabled:text-content-inverse " +
          "px-medium py-xsmall",
        ghost:
          "hover:bg-bg-fill-neutral-flat-hover active:bg-bg-fill-neutral-flat-press " +
          "text-content-neutral-strong disabled:text-content-disabled " +
          "px-medium py-xsmall",
        danger:
          "bg-bg-fill-negative-default hover:bg-bg-fill-negative-hover active:bg-bg-fill-negative-press " +
          "disabled:bg-bg-fill-disabled " +
          "text-content-inverse " +
          "px-medium py-xsmall",
        flat:
          "text-content-neutral-strong hover:text-content-neutral-medium " +
          "active:text-content-neutral-strong disabled:text-content-disabled " +
          "px-2xsmall py-0",
      },
      iconPosition: {
        none:  "gap-0",
        left:  "gap-2xsmall",
        right: "gap-2xsmall",
      },
    },
    defaultVariants: {
      variant: "primary",
      iconPosition: "none",
    },
  },
);
