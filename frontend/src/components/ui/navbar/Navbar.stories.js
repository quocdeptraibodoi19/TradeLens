import { useRouter } from 'vue-router'
import { Navbar } from './index.js'

export default {
  title: 'UI/Navbar',
  component: Navbar,
  tags: ['autodocs'],
  argTypes: {
    userName: { control: 'text', description: 'User name for avatar initials' },
    userSrc: { control: 'text', description: 'URL for user avatar image' },
  },
  args: {
    userName: 'Le Thanh',
  },
}

const makeRender = (path) => (args) => ({
  components: { Navbar },
  setup() {
    const router = useRouter()
    router.replace(path)
    return { args }
  },
  template: `<Navbar v-bind="args" />`,
})

export const HomeActive = {
  name: 'Home Active',
  render: makeRender('/home'),
}

export const OrdersActive = {
  name: 'Orders Active',
  render: makeRender('/orders'),
}

export const AlertsActive = {
  name: 'Alerts Active',
  render: makeRender('/alerts'),
}

export const NoActiveTab = {
  name: 'No Active Tab',
  render: makeRender('/other'),
}
