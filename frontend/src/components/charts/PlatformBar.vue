<template><div ref="el" class="chart"></div></template>
<script setup lang="ts">
import { useChart } from './useChart'
const props = defineProps<{ rows: Array<Record<string, any>> }>()
const el = useChart(() => ({
  tooltip: {},
  xAxis: { type: 'category', data: props.rows.map(i => i.platform) },
  yAxis: { type: 'value' },
  series: [{ type: 'bar', data: props.rows.map(i => i.count), itemStyle: { color: '#2563eb' } }]
}))
</script>
