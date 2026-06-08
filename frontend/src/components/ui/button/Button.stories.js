import Button from './Button.vue'

export default {
  title: 'UI/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'secondary', 'destructive', 'outline', 'ghost', 'link'],
    },
    size: {
      control: 'select',
      options: ['default', 'sm', 'lg', 'xs', 'icon'],
    },
  },
}

export const Default = {
  args: {
    variant: 'default',
  },
  render: (args) => ({
    components: { Button },
    setup() { return { args } },
    template: '<Button v-bind="args">Button</Button>',
  }),
}

export const Secondary = {
  args: {
    variant: 'secondary',
  },
  render: (args) => ({
    components: { Button },
    setup() { return { args } },
    template: '<Button v-bind="args">Button</Button>',
  }),
}

export const Destructive = {
  args: {
    variant: 'destructive',
  },
  render: (args) => ({
    components: { Button },
    setup() { return { args } },
    template: '<Button v-bind="args">Button</Button>',
  }),
}
