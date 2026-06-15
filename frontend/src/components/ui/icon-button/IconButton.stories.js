import IconButton from './IconButton.vue'

const VARIANTS = ['primary', 'ghost', 'danger-flat']
const STATES   = ['default', 'hover', 'press', 'disabled']

const PlusIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
         class="size-5">
      <path d="M12 5v14M5 12h14"/>
    </svg>
  `,
}

export default {
  title: 'UI/IconButton',
  component: IconButton,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      name: 'Variant',
      control: 'select',
      options: VARIANTS,
      description: 'Visual style of the icon button (Figma: Type property)',
    },
    state: {
      name: 'State',
      control: 'select',
      options: STATES,
      description:
        'default / hover / press are interactive CSS states — hover or click the button in the canvas. ' +
        'Selecting "disabled" sets the disabled HTML attribute.',
    },
  },
  args: {
    variant: 'primary',
    state: 'default',
  },
}

const render = (args) => ({
  components: { IconButton, PlusIcon },
  setup() { return { args } },
  template: `
    <IconButton
      :variant="args.variant"
      :disabled="args.state === 'disabled'"
    >
      <PlusIcon />
    </IconButton>
  `,
})

export const Default = { render }

export const Primary    = { args: { variant: 'primary'     }, render }
export const Ghost      = { args: { variant: 'ghost'       }, render }
export const DangerFlat = { args: { variant: 'danger-flat' }, render }

export const AllVariants = {
  name: 'All Variants',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { IconButton, PlusIcon },
    setup() { return { VARIANTS } },
    template: `
      <div class="flex flex-wrap gap-3 p-6 bg-bg-surface">
        <IconButton v-for="v in VARIANTS" :key="v" :variant="v">
          <PlusIcon />
        </IconButton>
      </div>
    `,
  }),
}

export const StatesMatrix = {
  name: 'States Matrix',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { IconButton, PlusIcon },
    setup() { return { VARIANTS } },
    template: `
      <div class="p-6 bg-bg-surface space-y-4">
        <div class="grid grid-cols-3 gap-3 w-fit">
          <span
            v-for="v in VARIANTS" :key="v"
            class="text-caption-strong text-content-neutral-medium text-center capitalize"
          >{{ v }}</span>
        </div>

        <!-- Default -->
        <div class="grid grid-cols-3 gap-3 w-fit items-center">
          <IconButton v-for="v in VARIANTS" :key="v" :variant="v">
            <PlusIcon />
          </IconButton>
        </div>

        <!-- Hover / Press (interactive) -->
        <div class="grid grid-cols-3 gap-3 w-fit items-center">
          <IconButton v-for="v in VARIANTS" :key="v" :variant="v">
            <PlusIcon />
          </IconButton>
        </div>

        <!-- Disabled -->
        <div class="grid grid-cols-3 gap-3 w-fit items-center">
          <IconButton v-for="v in VARIANTS" :key="v" :variant="v" disabled>
            <PlusIcon />
          </IconButton>
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
