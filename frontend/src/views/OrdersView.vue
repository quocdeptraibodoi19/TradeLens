<script setup>
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const orders = [
  { stock: "AAPL", side: "Buy", type: "Market", status: "Filled", date: "May 14, 09:31" },
  { stock: "AAPL", side: "Sell", type: "Market", status: "Pending", date: "May 14, 09:31" },
  { stock: "AAPL", side: "Sell", type: "Market", status: "Pending", date: "May 14, 09:31" },
  { stock: "AAPL", side: "Buy", type: "Market", status: "Canceled", date: "May 14, 09:31" },
  { stock: "AAPL", side: "Buy", type: "Market", status: "Rejected", date: "May 14, 09:31" },
];

const statusVariant = {
  Filled: "success",
  Pending: "warning",
  Canceled: "secondary",
  Rejected: "destructive",
};
</script>

<template>
  <div class="p-6">
    <h1 class="text-h3-strong mb-4">Orders</h1>
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
          <TableCell class="text-body-small-strong">{{ order.stock }}</TableCell>
          <TableCell>{{ order.side }}</TableCell>
          <TableCell>{{ order.type }}</TableCell>
          <TableCell>
            <Badge :variant="statusVariant[order.status]">{{ order.status }}</Badge>
          </TableCell>
          <TableCell class="text-right">{{ order.date }}</TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>
