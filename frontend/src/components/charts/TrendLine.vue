<template><div ref="el" class="chart"></div></template>
<script setup lang="ts">
import { useChart } from './useChart'
const props = defineProps<{ rows: Array<Record<string, any>> }>()
const el = useChart(() => ({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: props.rows.map(i => i.time) },
  yAxis: { type: 'value' },
  series: [{ type: 'line', smooth: true, data: props.rows.map(i => i.avg_sentiment_score), areaStyle: {}, itemStyle: { color: '#7c3aed' } }]
}))
</script>
