import { cva } from "class-variance-authority";

export { default as MetricWidget } from "./MetricWidget.vue";

export const metricWidgetVariants = cva(
  "content-stretch flex flex-col items-start gap-small p-xlarge relative rounded-xsmall w-[232px]",
  {
    variants: {
      variant: {
        indigo:  "bg-display-indigo-light  text-display-indigo-on-subtle",
        blue:    "bg-display-blue-light    text-display-blue-on-subtle",
        green:   "bg-display-green-light   text-display-green-on-subtle",
        yellow:  "bg-display-yellow-light  text-display-yellow-on-subtle",
        gray:    "bg-display-gray-light    text-display-gray-on-subtle",
        pink:    "bg-display-pink-light",
        red:     "bg-display-red-light     text-display-red-on-subtle",
        primary: "bg-display-primary-light text-display-primary-on-subtle",
      },
    },
    defaultVariants: { variant: "indigo" },
  }
);
