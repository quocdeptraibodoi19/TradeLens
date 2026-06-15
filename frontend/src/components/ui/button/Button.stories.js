import Button from './Button.vue'

const VARIANTS = ['primary', 'accent', 'ghost', 'danger', 'flat']
const STATES   = ['default', 'hover', 'press', 'disabled']

export default {
  title: 'UI/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      name: 'Type',
      control: 'select',
      options: VARIANTS,
      description: 'Visual style of the button (Figma: Type property)',
    },
    state: {
      name: 'State',
      control: 'select',
      options: STATES,
      description:
        'default / hover / press are interactive CSS states — hover or click the button in the canvas. ' +
        'Selecting "disabled" sets the disabled HTML attribute.',
    },
    iconPosition: {
      name: 'Icon Position',
      control: 'select',
      options: ['none', 'left', 'right'],
    },
  },
  args: {
    variant: 'primary',
    state: 'default',
    iconPosition: 'none',
  },
}

const render = (args) => ({
  components: { Button },
  setup() { return { args } },
  template: `
    <Button
      :variant="args.variant"
      :icon-position="args.iconPosition"
      :disabled="args.state === 'disabled'"
    >
      <template v-if="args.iconPosition !== 'none'" #icon>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             class="size-5">
          <path d="M12 5v14M5 12h14"/>
        </svg>
      </template>
      Button
    </Button>
  `,
})

export const Default = { render }

export const Primary   = { args: { variant: 'primary'  }, render }
export const Accent    = { args: { variant: 'accent'   }, render }
export const Ghost     = { args: { variant: 'ghost'    }, render }
export const Danger    = { args: { variant: 'danger'   }, render }
export const Flat      = { args: { variant: 'flat'     }, render }

export const WithIconLeft  = { args: { iconPosition: 'left'  }, render }
export const WithIconRight = { args: { iconPosition: 'right' }, render }

export const AllVariants = {
  name: 'All Variants',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { Button },
    setup() { return { VARIANTS } },
    template: `
      <div class="flex flex-wrap gap-3 p-6 bg-bg-surface">
        <Button v-for="v in VARIANTS" :key="v" :variant="v">{{ v }}</Button>
      </div>
    `,
  }),
}

export const StatesMatrix = {
  name: 'States Matrix',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { Button },
    setup() { return { VARIANTS } },
    template: `
      <div class="p-6 bg-bg-surface space-y-4">
        <div class="grid grid-cols-5 gap-3">
          <span
            v-for="v in VARIANTS" :key="v"
            class="text-caption-strong text-content-neutral-medium text-center capitalize"
          >{{ v }}</span>
        </div>

        <!-- Default -->
        <div class="grid grid-cols-5 gap-3 items-center">
          <Button v-for="v in VARIANTS" :key="v" :variant="v">Button</Button>
        </div>

        <!-- Hover (interactive — hover each button to see) -->
        <div class="grid grid-cols-5 gap-3 items-center">
          <Button v-for="v in VARIANTS" :key="v" :variant="v">Button</Button>
        </div>

        <!-- Disabled -->
        <div class="grid grid-cols-5 gap-3 items-center">
          <Button v-for="v in VARIANTS" :key="v" :variant="v" disabled>Button</Button>
        </div>

        <div class="flex gap-8 pt-2">
          <span class="text-caption-light text-content-neutral-light">Row 1: Default</span>
          <span class="text-caption-light text-content-neutral-light">Row 2: Hover / Press (interactive)</span>
          <span class="text-caption-light text-content-neutral-light">Row 3: Disabled</span>
        </div>
      </div>
    `,
  }),
}
