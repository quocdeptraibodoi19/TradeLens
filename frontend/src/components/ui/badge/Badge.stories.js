import Badge from './Badge.vue'

export default {
  title: 'UI/Badge',
  component: Badge,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      name: 'Variant',
      control: 'select',
      options: ['gray', 'blue', 'green', 'yellow', 'red'],
      description: 'Color appearance of the badge',
    },
    label: {
      name: 'Label',
      control: 'text',
      description: 'Text content of the badge',
    },
  },
  args: {
    variant: 'gray',
    label: 'Badge',
  },
}

const render = (args) => ({
  components: { Badge },
  setup() { return { args } },
  template: `<Badge :variant="args.variant">{{ args.label }}</Badge>`,
})

export const Default = { render }

export const Gray   = { args: { variant: 'gray'   }, render }
export const Blue   = { args: { variant: 'blue'   }, render }
export const Green  = { args: { variant: 'green'  }, render }
export const Yellow = { args: { variant: 'yellow' }, render }
export const Red    = { args: { variant: 'red'    }, render }

export const AllVariants = {
  name: 'All Variants',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { Badge },
    setup() {
      return {
        items: [
          { variant: 'gray',   label: 'Gray'   },
          { variant: 'blue',   label: 'Blue'   },
          { variant: 'green',  label: 'Green'  },
          { variant: 'yellow', label: 'Yellow' },
          { variant: 'red',    label: 'Red'    },
        ],
      }
    },
    template: `
      <div class="flex flex-wrap gap-6 p-6 bg-bg-surface items-end">
        <div v-for="item in items" :key="item.variant" class="flex flex-col items-center gap-2">
          <Badge :variant="item.variant">Badge</Badge>
          <span class="text-caption-light text-content-neutral-medium">{{ item.label }}</span>
        </div>
      </div>
    `,
  }),
}
