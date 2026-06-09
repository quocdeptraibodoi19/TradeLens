import { NavbarTab } from './index.js'

export default {
  title: 'UI/NavbarTab',
  component: NavbarTab,
  tags: ['autodocs'],
  argTypes: {
    label: {
      control: 'text',
      description: 'Tab label text',
    },
    selected: {
      control: 'boolean',
      description: 'Whether the tab is in the selected state',
    },
  },
  args: {
    label: 'Home',
    selected: false,
  },
}

const render = (args) => ({
  components: { NavbarTab },
  setup() { return { args } },
  template: `<NavbarTab :label="args.label" :selected="args.selected" />`,
})

export const Default  = { render }
export const Selected = { args: { selected: true }, render }

export const AllStates = {
  name: 'All States',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { NavbarTab },
    template: `
      <div class="flex items-center gap-2 p-6 bg-bg-surface">
        <NavbarTab label="Default" :selected="false" />
        <NavbarTab label="Selected" :selected="true" />
      </div>
    `,
  }),
}
