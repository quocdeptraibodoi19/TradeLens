import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './index.js'

// ── Status pill helper (inline, no Badge dependency) ──────────────────────────
const statusStyles = {
  Filled:   'bg-display-green-light   text-display-green-strong',
  Pending:  'bg-display-yellow-light  text-display-yellow-strong',
  Canceled: 'bg-display-gray-light    text-display-gray-strong',
  Rejected: 'bg-display-red-light     text-display-red-strong',
}

const ORDERS = [
  { stock: 'AAPL', side: 'Buy',  type: 'Market', status: 'Filled',   date: 'May 14, 09:31' },
  { stock: 'AAPL', side: 'Sell', type: 'Market', status: 'Pending',  date: 'May 14, 09:31' },
  { stock: 'AAPL', side: 'Sell', type: 'Market', status: 'Pending',  date: 'May 14, 09:31' },
  { stock: 'AAPL', side: 'Buy',  type: 'Market', status: 'Canceled', date: 'May 14, 09:31' },
  { stock: 'AAPL', side: 'Buy',  type: 'Market', status: 'Rejected', date: 'May 14, 09:31' },
]

const HOLDINGS = [
  { stock: 'AAPL', name: 'Apple Inc.',    qty: 12, value: '$2,268.00', pnl: '+$184.00', pnlPositive: true },
  { stock: 'MSFT', name: 'Microsoft',     qty: 8,  value: '$3,120.00', pnl: '+$420.00', pnlPositive: true },
  { stock: 'TSLA', name: 'Tesla Inc.',    qty: 5,  value: '$1,050.00', pnl: '-$86.00',  pnlPositive: false },
  { stock: 'AMZN', name: 'Amazon.com',    qty: 3,  value: '$5,430.00', pnl: '+$210.00', pnlPositive: true },
]

// ─────────────────────────────────────────────────────────────────────────────

export default {
  title: 'UI/Table',
  tags: ['autodocs'],
  argTypes: {
    align: {
      name: 'Header Align',
      control: 'select',
      options: ['left', 'right'],
      description: 'Alignment of the TableHead label and icon (Figma: Align property)',
    },
  },
  args: {
    align: 'left',
  },
}

// ── Single TableHead playground ───────────────────────────────────────────────
export const HeaderCell = {
  name: 'TableHead — Playground',
  argTypes: {
    align: {
      control: 'select',
      options: ['left', 'right'],
    },
    showIcon: {
      name: 'Show icon',
      control: 'boolean',
    },
    label: {
      name: 'Label',
      control: 'text',
    },
  },
  args: { align: 'left', showIcon: false, label: 'Stock' },
  render: (args) => ({
    components: { Table, TableHeader, TableRow, TableHead },
    setup() { return { args } },
    template: `
      <Table class="w-[320px]">
        <TableHeader>
          <TableRow>
            <TableHead :align="args.align">
              <template v-if="args.showIcon" #icon>
                <svg xmlns="http://www.w3.org/2000/svg" class="size-5 text-content-neutral-light" viewBox="0 0 24 24"
                     fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
                </svg>
              </template>
              {{ args.label }}
            </TableHead>
          </TableRow>
        </TableHeader>
      </Table>
    `,
  }),
}

// ── Alignment comparison ──────────────────────────────────────────────────────
export const HeaderAlignment = {
  name: 'TableHead — Alignment',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { Table, TableHeader, TableRow, TableHead },
    template: `
      <Table class="w-[480px]">
        <TableHeader>
          <TableRow>
            <TableHead align="left"  class="w-1/2">Stock (Left)</TableHead>
            <TableHead align="right" class="w-1/2">Quantity (Right)</TableHead>
          </TableRow>
        </TableHeader>
      </Table>
    `,
  }),
}

// ── Header with icon ──────────────────────────────────────────────────────────
export const HeaderWithIcon = {
  name: 'TableHead — With Icon',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { Table, TableHeader, TableRow, TableHead },
    template: `
      <Table class="w-[320px]">
        <TableHeader>
          <TableRow>
            <TableHead>
              <template #icon>
                <svg xmlns="http://www.w3.org/2000/svg" class="size-5 text-content-neutral-light" viewBox="0 0 24 24"
                     fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
                </svg>
              </template>
              Stock
            </TableHead>
          </TableRow>
        </TableHeader>
      </Table>
    `,
  }),
}

// ── Orders table (matches Figma example 1) ────────────────────────────────────
export const OrdersTable = {
  name: 'Orders Table',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { Table, TableHeader, TableBody, TableRow, TableHead, TableCell },
    setup() {
      return { ORDERS, statusStyles }
    },
    template: `
      <div class="p-6 bg-bg-surface rounded-xlarge">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Stock</TableHead>
              <TableHead>Side</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Status</TableHead>
              <TableHead align="right">Placed date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="(order, i) in ORDERS" :key="i">
              <TableCell class="text-body-small-strong">{{ order.stock }}</TableCell>
              <TableCell class="text-body-small-medium">{{ order.side }}</TableCell>
              <TableCell class="text-body-small-medium">{{ order.type }}</TableCell>
              <TableCell>
                <span
                  class="inline-flex items-center rounded-rounded px-small py-3xsmall text-caption-medium"
                  :class="statusStyles[order.status]"
                >{{ order.status }}</span>
              </TableCell>
              <TableCell class="text-body-small-medium text-right">{{ order.date }}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    `,
  }),
}

// ── Holdings table (matches Figma example 2) ──────────────────────────────────
export const HoldingsTable = {
  name: 'Holdings Table',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { Table, TableHeader, TableBody, TableRow, TableHead, TableCell },
    setup() {
      return { HOLDINGS }
    },
    template: `
      <div class="p-6 bg-bg-surface rounded-xlarge">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Stock</TableHead>
              <TableHead align="right">Quantity</TableHead>
              <TableHead align="right">Current value</TableHead>
              <TableHead align="right">Unrealized P&L</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="(h, i) in HOLDINGS" :key="i">
              <TableCell>
                <div class="flex flex-col gap-3xsmall">
                  <span class="text-body-small-strong">{{ h.stock }}</span>
                  <span class="text-caption-medium text-content-neutral-light">{{ h.name }}</span>
                </div>
              </TableCell>
              <TableCell class="text-body-small-medium text-right">{{ h.qty }}</TableCell>
              <TableCell class="text-body-small-strong text-right">{{ h.value }}</TableCell>
              <TableCell
                class="text-body-small-strong text-right"
                :class="h.pnlPositive ? 'text-display-green-strong' : 'text-display-red-strong'"
              >{{ h.pnl }}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    `,
  }),
}

// ── TableCell playground ──────────────────────────────────────────────────────
export const CellPlayground = {
  name: 'TableCell — Playground',
  argTypes: {
    content: {
      name: 'Content',
      control: 'select',
      options: ['Plain text', 'Bold text', 'Two-line (ticker + name)', 'Number', 'Custom badge'],
    },
  },
  args: { content: 'Plain text' },
  render: (args) => ({
    components: { Table, TableBody, TableHead, TableHeader, TableRow, TableCell },
    setup() { return { args } },
    template: `
      <Table class="w-[320px]">
        <TableHeader>
          <TableRow>
            <TableHead>Column</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow>
            <TableCell>
              <span v-if="args.content === 'Plain text'" class="text-body-small-medium">Market</span>
              <span v-else-if="args.content === 'Bold text'" class="text-body-small-strong">AAPL</span>
              <span v-else-if="args.content === 'Number'" class="text-body-small-strong">$2,268.00</span>
              <div v-else-if="args.content === 'Two-line (ticker + name)'" class="flex flex-col gap-3xsmall">
                <span class="text-body-small-strong">AAPL</span>
                <span class="text-caption-medium text-content-neutral-light">Apple Inc.</span>
              </div>
              <span v-else class="inline-flex items-center rounded-rounded px-small py-3xsmall text-caption-medium bg-display-green-light text-display-green-strong">Filled</span>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    `,
  }),
}

// ── TableCell content variants ────────────────────────────────────────────────
export const CellContentVariants = {
  name: 'TableCell — Content Variants',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { Table, TableBody, TableHead, TableHeader, TableRow, TableCell },
    template: `
      <div class="p-6 bg-bg-surface rounded-xlarge">
        <Table class="w-[320px]">
          <TableHeader>
            <TableRow>
              <TableHead>Content type</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell>
                <span class="text-body-small-medium">Plain text (Market)</span>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>
                <span class="text-body-small-strong">Bold text (AAPL)</span>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>
                <div class="flex flex-col gap-3xsmall">
                  <span class="text-body-small-strong">AAPL</span>
                  <span class="text-caption-medium text-content-neutral-light">Apple Inc.</span>
                </div>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>
                <span class="text-body-small-strong text-display-green-strong">+$184.00</span>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>
                <span class="inline-flex items-center rounded-rounded px-small py-3xsmall text-caption-medium bg-display-green-light text-display-green-strong">Filled</span>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    `,
  }),
}

// ── Row hover demonstration ───────────────────────────────────────────────────
export const RowHover = {
  name: 'TableCell — Row Hover',
  parameters: { controls: { disable: true } },
  render: () => ({
    components: { Table, TableHeader, TableBody, TableRow, TableHead, TableCell },
    template: `
      <div class="p-6 bg-bg-surface rounded-xlarge">
        <p class="text-caption-medium text-content-neutral-light mb-4">Hover over any row to see the highlight effect.</p>
        <Table class="w-[480px]">
          <TableHeader>
            <TableRow>
              <TableHead>Stock</TableHead>
              <TableHead>Side</TableHead>
              <TableHead align="right">Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="n in 4" :key="n">
              <TableCell class="text-body-small-strong">AAPL</TableCell>
              <TableCell class="text-body-small-medium">Buy</TableCell>
              <TableCell class="text-body-small-medium text-right">May 14, 09:31</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    `,
  }),
}
