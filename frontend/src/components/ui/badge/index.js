import { cva } from "class-variance-authority";

export { default as Badge } from "./Badge.vue";

export const badgeVariants = cva(
  "inline-flex w-fit shrink-0 items-center justify-center whitespace-nowrap " +
  "rounded-rounded px-small py-3xsmall text-body-small-medium",
  {
    variants: {
      variant: {
        gray:   "bg-display-gray-light   text-display-gray-strong",
        blue:   "bg-display-blue-light   text-display-blue-strong",
        green:  "bg-display-green-light  text-display-green-strong",
        yellow: "bg-display-yellow-light text-display-yellow-strong",
        red:    "bg-display-red-light    text-display-red-strong",
      },
    },
    defaultVariants: { variant: "gray" },
  },
);
