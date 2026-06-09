import Avatar from './Avatar.vue'

const SAMPLE_IMAGE = 'https://i.pravatar.cc/48'

export default {
  title: 'UI/Avatar',
  component: Avatar,
  tags: ['autodocs'],
  argTypes: {
    name: {
      name: 'Name',
      control: 'text',
      description: 'Full name — initials are derived from the first and last word',
    },
    src: {
      name: 'Image URL',
      control: 'text',
      description: 'When provided, shows a photo instead of initials',
    },
    alt: {
      name: 'Alt text',
      control: 'text',
      description: 'Alt text for the image (used when src is set)',
    },
  },
  args: {
    name: 'Le Trong',
    src: '',
    alt: '',
  },
}

const render = (args) => ({
  components: { Avatar },
  setup() { return { args } },
  template: `
    <Avatar
      :name="args.name"
      :src="args.src || undefined"
      :alt="args.alt"
    />
  `,
})

export const Default = { render }

export const TextOnly = {
  args: { name: 'Le Trong', src: '' },
  render,
}

export const WithImage = {
  args: { name: 'Le Trong', src: SAMPLE_IMAGE, alt: 'Le Trong' },
  render,
}

export const SingleName = {
  args: { name: 'Trang', src: '' },
  render,
}

export const AllVariants = {
  name: 'All Variants',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { Avatar },
    setup() {
      return {
        items: [
          { name: 'Le Trong',  src: undefined,      label: 'Text initials' },
          { name: 'Le Trong',  src: SAMPLE_IMAGE,   label: 'With image'    },
          { name: 'Trang',     src: undefined,      label: 'Single name'   },
        ],
      }
    },
    template: `
      <div class="flex flex-wrap gap-6 p-6 bg-bg-surface items-end">
        <div v-for="item in items" :key="item.label" class="flex flex-col items-center gap-2">
          <Avatar :name="item.name" :src="item.src" :alt="item.name" />
          <span class="text-caption-light text-content-neutral-medium">{{ item.label }}</span>
        </div>
      </div>
    `,
  }),
}
