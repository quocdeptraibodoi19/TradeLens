<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { Button } from '@/components/ui/button'
import {
  Table,
  TableBody,
  TableCell,
  TableEmpty,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { fetchAccountOverview, fetchHoldings, syncDashboard } from '@/api'

const TOP_HOLDINGS = 5
const SYNC_POLL_MS = 1500
const SYNC_POLL_TRIES = 10

const account = ref(null)
const holdings = ref([])
const holdingsTotal = ref(0)
const holdingsBatchedAt = ref(null)
const errors = ref({ account: null, holdings: null })
const loading = ref(true)
const syncing = ref(false)
const notAuthenticated = ref(false)
const now = ref(Date.now())

// --- formatting -------------------------------------------------------------

const usd = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })
const qtyFmt = new Intl.NumberFormat('en-US', { maximumFractionDigits: 4 })

function formatCurrency(v) {
  return v == null ? '—' : usd.format(Number(v))
}

function formatSignedCurrency(v) {
  if (v == null) return '—'
  const n = Number(v)
  return (n > 0 ? '+' : '') + usd.format(n)
}

function formatQty(v) {
  return v == null ? '—' : qtyFmt.format(Number(v))
}

// The API stores UTC but may send timestamps without an offset; without one,
// the browser would read them as local time.
function parseUtc(ts) {
  if (!ts) return null
  const hasOffset = /(Z|[+-]\d{2}:?\d{2})$/.test(ts)
  return new Date(hasOffset ? ts : `${ts}Z`)
}

function timeAgo(date) {
  if (!date) return null
  const seconds = Math.max(0, Math.round((now.value - date.getTime()) / 1000))
  if (seconds < 60) return `${seconds} seconds ago`
  const minutes = Math.round(seconds / 60)
  if (minutes < 60) return `${minutes} minute${minutes === 1 ? '' : 's'} ago`
  const hours = Math.round(minutes / 60)
  if (hours < 24) return `${hours} hour${hours === 1 ? '' : 's'} ago`
  return date.toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

// --- derived state ----------------------------------------------------------

const lastUpdated = computed(() => {
  const dates = [parseUtc(account.value?.batched_at), parseUtc(holdingsBatchedAt.value)].filter(Boolean)
  if (!dates.length) return null
  return timeAgo(new Date(Math.min(...dates.map(d => d.getTime()))))
})

const todayChange = computed(() => {
  const equity = Number(account.value?.equity)
  const last = Number(account.value?.last_equity)
  if (!account.value || !last) return null
  const diff = equity - last
  return { diff, pct: diff / last }
})

// Invested vs cash share of the portfolio. Cash can go negative on margin,
// so clamp each share to [0, 1].
const allocation = computed(() => {
  const total = Number(account.value?.portfolio_value)
  if (!account.value || !total) return null
  const cash = Number(account.value.cash)
  const invested = total - cash
  const clamp = v => Math.min(1, Math.max(0, v))
  return {
    segments: [
      { key: 'invested', label: 'Invested', value: invested, share: clamp(invested / total), color: 'bg-display-indigo-default' },
      { key: 'cash',     label: 'Cash',     value: cash,     share: clamp(cash / total),     color: 'bg-display-pink-default' },
    ],
    onMargin: cash < 0,
  }
})

function holdingShare(h) {
  const total = Number(account.value?.portfolio_value)
  if (!total || h.market_value == null) return null
  return Math.max(0, Number(h.market_value) / total)
}

function formatShare(share) {
  if (share > 0 && share < 0.001) return '<0.1%'
  return pctFmt.format(share)
}

function plPct(h) {
  if (h.market_value == null || h.unrealized_pl == null) return null
  const cost = Number(h.market_value) - Number(h.unrealized_pl)
  return cost ? Number(h.unrealized_pl) / cost : null
}

const pctFmt = new Intl.NumberFormat('en-US', { style: 'percent', maximumFractionDigits: 1 })
const signedPctFmt = new Intl.NumberFormat('en-US', { style: 'percent', maximumFractionDigits: 2, signDisplay: 'exceptZero' })

const secondaryCards = computed(() => [
  { label: 'Equity',       icon: 'fa-solid fa-scale-balanced', value: formatCurrency(account.value?.equity) },
  { label: 'Cash balance', icon: 'fa-solid fa-wallet',         value: formatCurrency(account.value?.cash) },
  { label: 'Buying power', icon: 'fa-solid fa-bolt',           value: formatCurrency(account.value?.buying_power) },
])

const neverSynced = computed(() => errors.value.account?.status === 404)

const partialFailure = computed(() => {
  const failed = Object.values(errors.value).filter(e => e && e.status !== 404 && e.status !== 401)
  return failed.length > 0
})

// --- data loading -----------------------------------------------------------

async function load() {
  const [accountRes, holdingsRes] = await Promise.allSettled([
    fetchAccountOverview(),
    fetchHoldings(TOP_HOLDINGS),
  ])

  errors.value = {
    account: accountRes.status === 'rejected' ? accountRes.reason : null,
    holdings: holdingsRes.status === 'rejected' ? holdingsRes.reason : null,
  }
  notAuthenticated.value = Object.values(errors.value).some(e => e?.status === 401)

  account.value = accountRes.status === 'fulfilled' ? accountRes.value : null
  if (holdingsRes.status === 'fulfilled') {
    holdings.value = holdingsRes.value.holdings
    holdingsTotal.value = holdingsRes.value.total
    holdingsBatchedAt.value = holdingsRes.value.batched_at
  } else {
    holdings.value = []
    holdingsTotal.value = 0
    holdingsBatchedAt.value = null
  }
}

// Sync runs in a background worker, so poll until a newer snapshot shows up.
async function refresh() {
  syncing.value = true
  try {
    const before = account.value?.batched_at ?? null
    await syncDashboard()
    for (let i = 0; i < SYNC_POLL_TRIES; i++) {
      await new Promise(r => setTimeout(r, SYNC_POLL_MS))
      await load()
      if (account.value?.batched_at && account.value.batched_at !== before) break
    }
  } catch (e) {
    errors.value = { ...errors.value, account: e }
    notAuthenticated.value = e.status === 401
  } finally {
    syncing.value = false
  }
}

let clock
onMounted(async () => {
  clock = setInterval(() => (now.value = Date.now()), 15000)
  try {
    await load()
  } finally {
    loading.value = false
  }
})
onUnmounted(() => clearInterval(clock))
</script>

<template>
  <div class="flex flex-col gap-xlarge">
    <!-- Partial failure banner -->
    <div
      v-if="partialFailure"
      role="status"
      class="flex items-center gap-small rounded-xsmall bg-display-yellow-light px-medium py-small text-body-small-medium text-display-yellow-strong"
    >
      <font-awesome-icon icon="fa-solid fa-triangle-exclamation" />
      Some data could not be loaded. Showing partial information.
    </div>

    <!-- Page header -->
    <div class="flex flex-wrap items-end justify-between gap-medium">
      <div class="flex flex-col gap-2xsmall">
        <h1 class="text-display-medium">Dashboard</h1>
        <div class="flex items-center gap-xsmall text-body-small-medium text-content-neutral-light">
          <span class="relative flex size-2">
            <span
              v-if="syncing"
              class="absolute inline-flex size-full animate-ping rounded-rounded bg-display-green-default opacity-75"
            />
            <span
              class="relative inline-flex size-2 rounded-rounded"
              :class="lastUpdated ? 'bg-display-green-default' : 'bg-display-gray-default'"
            />
          </span>
          <span v-if="syncing">Syncing with Alpaca…</span>
          <span v-else-if="lastUpdated">Last updated {{ lastUpdated }}</span>
          <span v-else>Not synced yet</span>
        </div>
      </div>
      <div class="flex gap-small">
        <Button variant="ghost" iconPosition="left" :disabled="syncing" @click="refresh">
          <template #icon>
            <font-awesome-icon icon="fa-solid fa-arrows-rotate" :spin="syncing" />
          </template>
          {{ syncing ? 'Syncing…' : 'Refresh' }}
        </Button>
        <Button variant="ghost" iconPosition="left" as="a" href="/auth/alpaca/connect">
          <template #icon>
            <font-awesome-icon icon="fa-solid fa-link" />
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

    <!-- Not logged in -->
    <div
      v-if="notAuthenticated"
      class="flex flex-col items-center gap-medium rounded-small border border-border-default bg-bg-surface px-xlarge py-4xlarge text-center"
    >
      <font-awesome-icon icon="fa-solid fa-lock" class="text-[32px] text-content-neutral-light" />
      <p class="text-h3-strong">You're not logged in</p>
      <p class="text-body-medium text-content-neutral-light">Log in to see your portfolio.</p>
      <Button variant="accent" :as="RouterLink" to="/login">Log in</Button>
    </div>

    <template v-else>
      <!-- Never synced -->
      <div
        v-if="neverSynced && !syncing"
        class="flex items-center gap-medium rounded-small border border-dashed border-border-default bg-bg-surface px-xlarge py-large"
      >
        <span class="flex size-10 shrink-0 items-center justify-center rounded-rounded bg-display-indigo-light text-display-indigo-strong">
          <font-awesome-icon icon="fa-solid fa-cloud-arrow-down" />
        </span>
        <div class="flex-1">
          <p class="text-body-strong">No data yet</p>
          <p class="text-body-small-medium text-content-neutral-light">
            Connect your Alpaca account, then sync to pull your portfolio.
          </p>
        </div>
        <Button variant="accent" @click="refresh">Sync now</Button>
      </div>

      <!-- Overview: hero + secondary KPIs -->
      <div class="grid grid-cols-1 gap-large lg:grid-cols-3">
        <!-- Hero -->
        <section class="relative overflow-hidden rounded-small border border-border-default bg-bg-surface p-xlarge lg:col-span-2">
          <div class="pointer-events-none absolute -right-24 -top-24 size-72 rounded-rounded bg-display-indigo-light blur-2xl" />
          <div class="relative flex h-full flex-col justify-between gap-large">
            <div class="flex flex-col gap-2xsmall">
              <p class="text-body-small-medium text-content-neutral-light">Portfolio value</p>
              <div class="flex flex-wrap items-baseline gap-medium">
                <p v-if="loading" class="h-12 w-64 animate-pulse rounded-xsmall bg-display-gray-light" />
                <p v-else class="text-display-strong tabular-nums">{{ formatCurrency(account?.portfolio_value) }}</p>
                <span
                  v-if="todayChange"
                  class="inline-flex items-center gap-2xsmall rounded-rounded px-small py-3xsmall text-body-small-strong tabular-nums"
                  :class="todayChange.diff >= 0
                    ? 'bg-display-green-light text-display-green-strong'
                    : 'bg-display-red-light text-display-red-strong'"
                >
                  <font-awesome-icon :icon="todayChange.diff >= 0 ? 'fa-solid fa-arrow-trend-up' : 'fa-solid fa-arrow-trend-down'" />
                  {{ formatSignedCurrency(todayChange.diff) }} ({{ signedPctFmt.format(todayChange.pct) }})
                  <span class="font-normal opacity-80">today</span>
                </span>
              </div>
            </div>

            <!-- Allocation bar -->
            <div v-if="allocation" class="flex flex-col gap-small">
              <div class="flex items-center justify-between text-body-small-medium text-content-neutral-light">
                <span>Allocation</span>
                <span v-if="allocation.onMargin" class="text-display-yellow-strong">
                  <font-awesome-icon icon="fa-solid fa-triangle-exclamation" /> Using margin
                </span>
              </div>
              <div
                class="flex h-3 w-full gap-[2px] overflow-hidden rounded-rounded"
                role="img"
                :aria-label="allocation.segments.map(s => `${s.label} ${pctFmt.format(s.share)}`).join(', ')"
              >
                <div
                  v-for="seg in allocation.segments.filter(s => s.share > 0)"
                  :key="seg.key"
                  class="group relative h-full transition-[width] duration-700 ease-out first:rounded-l-rounded last:rounded-r-rounded"
                  :class="seg.color"
                  :style="{ width: `${seg.share * 100}%` }"
                >
                  <span class="pointer-events-none absolute bottom-full left-1/2 mb-xsmall -translate-x-1/2 whitespace-nowrap rounded-3xsmall bg-content-neutral-strong px-xsmall py-3xsmall text-caption-medium text-content-inverse opacity-0 transition-opacity group-hover:opacity-100">
                    {{ seg.label }} · {{ formatCurrency(seg.value) }}
                  </span>
                </div>
              </div>
              <div class="flex flex-wrap gap-large">
                <div v-for="seg in allocation.segments" :key="seg.key" class="flex items-center gap-xsmall">
                  <span class="size-2.5 rounded-[3px]" :class="seg.color" />
                  <span class="text-body-small-medium text-content-neutral-light">{{ seg.label }}</span>
                  <span class="text-body-small-strong tabular-nums">{{ formatCurrency(seg.value) }}</span>
                  <span class="text-body-small-medium text-content-neutral-light tabular-nums">{{ pctFmt.format(seg.share) }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Secondary KPIs -->
        <div class="grid grid-cols-1 gap-medium sm:grid-cols-3 lg:grid-cols-1">
          <div
            v-for="card in secondaryCards"
            :key="card.label"
            class="flex items-center gap-medium rounded-small border border-border-default bg-bg-surface px-large py-medium transition-shadow hover:shadow-md"
          >
            <span class="flex size-10 shrink-0 items-center justify-center rounded-xsmall bg-display-primary-light text-display-primary-on-subtle">
              <font-awesome-icon :icon="card.icon" />
            </span>
            <div class="flex min-w-0 flex-col">
              <span class="text-body-small-medium text-content-neutral-light">{{ card.label }}</span>
              <span v-if="loading" class="mt-3xsmall h-6 w-28 animate-pulse rounded-3xsmall bg-display-gray-light" />
              <span v-else class="text-h3-strong tabular-nums">{{ card.value }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Holdings + orders -->
      <div class="grid grid-cols-1 gap-large xl:grid-cols-5">
        <!-- Top holdings -->
        <section class="flex flex-col rounded-small border border-border-default bg-bg-surface p-large xl:col-span-3">
          <div class="mb-medium flex items-center justify-between">
            <div class="flex items-baseline gap-small">
              <h2 class="text-h3-strong">Top holdings</h2>
              <span v-if="holdingsTotal" class="text-body-small-medium text-content-neutral-light">
                {{ holdings.length }} of {{ holdingsTotal }}
              </span>
            </div>
            <router-link to="/portfolio" class="text-body-small-medium text-content-neutral-light hover:text-content-neutral-strong hover:underline">
              View all →
            </router-link>
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Stock</TableHead>
                <TableHead align="right">Qty</TableHead>
                <TableHead align="right">Current value</TableHead>
                <TableHead>Allocation</TableHead>
                <TableHead align="right">Unrealized P&amp;L</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <template v-if="loading">
                <TableRow v-for="i in 3" :key="i">
                  <TableCell v-for="j in 5" :key="j">
                    <div class="h-4 animate-pulse rounded-3xsmall bg-display-gray-light" />
                  </TableCell>
                </TableRow>
              </template>
              <TableEmpty v-else-if="errors.holdings" :colspan="5">Couldn't load holdings.</TableEmpty>
              <TableEmpty v-else-if="!holdings.length" :colspan="5">
                <div class="flex flex-col items-center gap-xsmall text-content-neutral-light">
                  <font-awesome-icon icon="fa-solid fa-briefcase" class="text-[24px]" />
                  No holdings yet
                </div>
              </TableEmpty>
              <TableRow v-for="h in holdings" v-else :key="h.symbol" class="transition-colors hover:bg-display-gray-light">
                <TableCell>
                  <div class="flex items-center gap-small">
                    <span class="flex size-8 shrink-0 items-center justify-center rounded-rounded bg-display-indigo-light text-caption-strong text-display-indigo-strong">
                      {{ h.symbol.slice(0, 2) }}
                    </span>
                    <span class="text-body-small-strong">{{ h.symbol }}</span>
                  </div>
                </TableCell>
                <TableCell class="text-right tabular-nums">{{ formatQty(h.qty) }}</TableCell>
                <TableCell class="text-right tabular-nums">{{ formatCurrency(h.market_value) }}</TableCell>
                <TableCell>
                  <div v-if="holdingShare(h) != null" class="flex items-center gap-small">
                    <div class="h-1.5 w-20 overflow-hidden rounded-rounded bg-display-gray-light">
                      <div
                        class="h-full rounded-rounded bg-display-indigo-default transition-[width] duration-700 ease-out"
                        :style="{ width: `${Math.min(1, holdingShare(h)) * 100}%` }"
                      />
                    </div>
                    <span class="text-caption-medium text-content-neutral-light tabular-nums">{{ formatShare(holdingShare(h)) }}</span>
                  </div>
                  <span v-else class="text-content-neutral-light">—</span>
                </TableCell>
                <TableCell class="text-right">
                  <div
                    class="flex flex-col items-end tabular-nums"
                    :class="Number(h.unrealized_pl) >= 0 ? 'text-display-green-strong' : 'text-display-red-strong'"
                  >
                    <span class="text-body-small-strong">
                      <font-awesome-icon
                        :icon="Number(h.unrealized_pl) >= 0 ? 'fa-solid fa-caret-up' : 'fa-solid fa-caret-down'"
                        class="mr-3xsmall"
                      />{{ formatSignedCurrency(h.unrealized_pl) }}
                    </span>
                    <span v-if="plPct(h) != null" class="text-caption-medium opacity-80">{{ signedPctFmt.format(plPct(h)) }}</span>
                  </div>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </section>

        <!-- Recent orders: no backend endpoint yet (orders ingestion is planned) -->
        <section class="flex flex-col rounded-small border border-border-default bg-bg-surface p-large xl:col-span-2">
          <div class="mb-medium flex items-center justify-between">
            <h2 class="text-h3-strong">Recent orders</h2>
            <router-link to="/orders" class="text-body-small-medium text-content-neutral-light hover:text-content-neutral-strong hover:underline">
              View all →
            </router-link>
          </div>
          <div class="flex flex-1 flex-col items-center justify-center gap-small rounded-xsmall border border-dashed border-border-default px-large py-3xlarge text-center">
            <span class="flex size-10 items-center justify-center rounded-rounded bg-display-pink-light text-display-pink-strong">
              <font-awesome-icon icon="fa-solid fa-receipt" />
            </span>
            <p class="text-body-strong">Coming soon</p>
            <p class="text-body-small-medium text-content-neutral-light">
              Order history will appear here once orders are synced.
            </p>
          </div>
        </section>
      </div>
    </template>
  </div>
</template>
