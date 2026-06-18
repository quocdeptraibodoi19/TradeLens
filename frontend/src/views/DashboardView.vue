<script setup>
import { Button } from '@/components/ui/button'
import { MetricWidget } from '@/components/ui/metric-widget'
import { Badge } from '@/components/ui/badge'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

const account = {
  portfolio_value: 24810,
  equity: 24810,
  cash_balance: 24810,
  buying_power: 24810,
}

const holdings = [
  { symbol: 'AAPL', company: 'Apple Inc.', quantity: 12, current_value: 2268.00, unrealized_pnl: 184.00 },
  { symbol: 'AAPL', company: 'Apple Inc.', quantity: 12, current_value: 2268.00, unrealized_pnl: 184.00 },
  { symbol: 'AAPL', company: 'Apple Inc.', quantity: 12, current_value: 2268.00, unrealized_pnl: 184.00 },
  { symbol: 'AAPL', company: 'Apple Inc.', quantity: 12, current_value: 2268.00, unrealized_pnl: 184.00 },
  { symbol: 'AAPL', company: 'Apple Inc.', quantity: 12, current_value: 2268.00, unrealized_pnl: 184.00 },
]

const orders = [
  { symbol: 'AAPL', side: 'Buy',  order_type: 'Market', status: 'Filled',   placed_date: 'May 14, 09:31' },
  { symbol: 'AAPL', side: 'Sell', order_type: 'Market', status: 'Pending',  placed_date: 'May 14, 09:31' },
  { symbol: 'AAPL', side: 'Sell', order_type: 'Market', status: 'Pending',  placed_date: 'May 14, 09:31' },
  { symbol: 'AAPL', side: 'Buy',  order_type: 'Market', status: 'Canceled', placed_date: 'May 14, 09:31' },
  { symbol: 'AAPL', side: 'Buy',  order_type: 'Market', status: 'Rejected', placed_date: 'May 14, 09:31' },
]

function formatCurrency(n) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2 })
}

const accountCards = [
  { label: 'Portfolio value', value: formatCurrency(account.portfolio_value) },
  { label: 'Equity',          value: formatCurrency(account.equity) },
  { label: 'Cash balance',    value: formatCurrency(account.cash_balance) },
  { label: 'Buying power',    value: formatCurrency(account.buying_power) },
]

const statusVariant = {
  Filled:   'green',
  Pending:  'yellow',
  Canceled: 'gray',
  Rejected: 'red',
}
</script>

<template>
  <div>
    <!-- Page header -->
    <div class="flex items-center justify-between">
      <h1 class="text-display-medium">Dashboard</h1>
      <div class="flex gap-small">
        <Button variant="ghost" iconPosition="left">
          <template #icon>
            <font-awesome-icon icon="fa-regular fa-arrows-rotate" />
          </template>
          Refresh
        </Button>
        <Button variant="ghost" iconPosition="left" as="a" href="/auth/alpaca/connect">
          <template #icon>
            <font-awesome-icon icon="fa-regular fa-link" />
          </template>
          Connect Alpaca
        </Button>
        <Button variant="accent" iconPosition="left">
          <template #icon>
            <font-awesome-icon icon="fa-regular fa-comment-dots" />
          </template>
          Ask AI
        </Button>
      </div>
    </div>

    <hr class="border-border-default my-xlarge" />

    <!-- Account overview -->
    <div class="flex gap-[24px]">
      <MetricWidget
        v-for="card in accountCards"
        :key="card.label"
        variant="primary"
        class="flex-1 w-auto"
        :label="card.label"
        :value="card.value"
      />
    </div>

    <!-- Two-column grid -->
    <div class="grid grid-cols-2 gap-[24px] mt-[48px]">

      <!-- Top holdings -->
      <div class="h-[392px] rounded-xsmall border border-border-default bg-bg-surface-default p-medium flex flex-col overflow-hidden">
        <div class="flex items-center justify-between mb-small">
          <h2 class="text-h3-strong">Top holdings</h2>
          <router-link to="/portfolio" class="text-body-small-medium text-content-neutral-light hover:underline">
            View all →
          </router-link>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Stock</TableHead>
              <TableHead>Quantity</TableHead>
              <TableHead>Current value</TableHead>
              <TableHead align="right">Unrealized P&amp;L</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="(h, i) in holdings" :key="i">
              <TableCell>
                <div class="flex flex-col">
                  <span class="text-body-small-strong">{{ h.symbol }}</span>
                  <span class="text-body-small-light text-content-neutral-light">{{ h.company }}</span>
                </div>
              </TableCell>
              <TableCell>{{ h.quantity }}</TableCell>
              <TableCell>{{ formatCurrency(h.current_value) }}</TableCell>
              <TableCell
                class="text-right"
                :class="h.unrealized_pnl >= 0 ? 'text-display-green-strong' : 'text-display-red-strong'"
              >
                {{ h.unrealized_pnl >= 0 ? '+' : '' }}{{ formatCurrency(h.unrealized_pnl) }}
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>

      <!-- Recent orders -->
      <div class="h-[392px] rounded-xsmall border border-border-default bg-bg-surface-default p-medium flex flex-col overflow-hidden">
        <div class="flex items-center justify-between mb-small">
          <h2 class="text-h3-strong">Recent orders</h2>
          <router-link to="/orders" class="text-body-small-medium text-content-neutral-light hover:underline">
            View all →
          </router-link>
        </div>
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
            <TableRow v-for="(order, i) in orders" :key="i">
              <TableCell class="text-body-small-strong">{{ order.symbol }}</TableCell>
              <TableCell>{{ order.side }}</TableCell>
              <TableCell>{{ order.order_type }}</TableCell>
              <TableCell>
                <Badge :variant="statusVariant[order.status]">{{ order.status }}</Badge>
              </TableCell>
              <TableCell class="text-right">{{ order.placed_date }}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>

    </div>
  </div>
</template>
