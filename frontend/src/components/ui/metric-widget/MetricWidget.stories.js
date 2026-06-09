import MetricWidget from './MetricWidget.vue'

export default {
  title: 'UI/MetricWidget',
  component: MetricWidget,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      name: 'Variant',
      control: 'select',
      options: ['indigo', 'blue', 'green', 'yellow', 'gray', 'pink', 'red', 'primary'],
      description: 'Color appearance of the metric widget',
    },
    label: {
      name: 'Label',
      control: 'text',
      description: 'Label text above the metric value',
    },
    value: {
      name: 'Value',
      control: 'text',
      description: 'The metric value to display',
    },
  },
  args: {
    variant: 'indigo',
    label: 'Label',
    value: '$24,810',
  },
}

const render = (args) => ({
  components: { MetricWidget },
  setup() { return { args } },
  template: `<MetricWidget :variant="args.variant" :label="args.label" :value="args.value" />`,
})

export const Default = { render }

export const Indigo  = { args: { variant: 'indigo'  }, render }
export const Blue    = { args: { variant: 'blue'    }, render }
export const Green   = { args: { variant: 'green'   }, render }
export const Yellow  = { args: { variant: 'yellow'  }, render }
export const Gray    = { args: { variant: 'gray'    }, render }
export const Pink    = { args: { variant: 'pink'    }, render }
export const Red     = { args: { variant: 'red'     }, render }
export const Primary = { args: { variant: 'primary' }, render }

export const AllVariants = {
  name: 'All Variants',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { MetricWidget },
    setup() {
      return {
        items: [
          { variant: 'indigo',  label: 'Indigo'  },
          { variant: 'blue',    label: 'Blue'    },
          { variant: 'green',   label: 'Green'   },
          { variant: 'yellow',  label: 'Yellow'  },
          { variant: 'gray',    label: 'Gray'    },
          { variant: 'pink',    label: 'Pink'    },
          { variant: 'red',     label: 'Red'     },
          { variant: 'primary', label: 'Primary' },
        ],
      }
    },
    template: `
      <div class="flex flex-wrap gap-6 p-6 bg-bg-surface">
        <div v-for="item in items" :key="item.variant" class="flex flex-col items-center gap-2">
          <MetricWidget :variant="item.variant" label="Total Volume" value="$24,810" />
          <span class="text-caption-light text-content-neutral-medium">{{ item.label }}</span>
        </div>
      </div>
    `,
  }),
}
