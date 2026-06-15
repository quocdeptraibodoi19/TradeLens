import '../src/style.css'
import { setup } from '@storybook/vue3'
import { createRouter, createMemoryHistory } from 'vue-router'

export const storybookRouter = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', redirect: '/home' },
    { path: '/:pathMatch(.*)*', component: { template: '<div />' } },
  ],
})

setup((app) => {
  app.use(storybookRouter)
})

/** @type { import('@storybook/vue3-vite').Preview } */
const preview = {
  parameters: {
    controls: {
      matchers: {
       color: /(background|color)$/i,
       date: /Date$/i,
      },
    },

    a11y: {
      // 'todo' - show a11y violations in the test UI only
      // 'error' - fail CI on a11y violations
      // 'off' - skip a11y checks entirely
      test: "todo"
    }
  },
};

export default preview;