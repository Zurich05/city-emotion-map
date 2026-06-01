<template><div ref="el" class="chart"></div></template>
<script setup lang="ts">
import { useChart } from './useChart'
const props = defineProps<{ rows: Array<Record<string, any>> }>()
const el = useChart(() => ({
  tooltip: { trigger: 'axis' },
  xAxis: {
    type: 'category',
    data: props.rows.map(i => i.time),
    axisLine: { lineStyle: { color: '#dbe5ef' } },
    axisLabel: { color: '#475569', fontSize: 14 }
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: '#edf2f7' } },
    axisLabel: { color: '#475569', fontSize: 14 }
  },
  series: [
    {
      name: '情绪指数',
      type: 'line',
      smooth: true,
      data: props.rows.map(i => i.avg_sentiment_score),
      symbolSize: 8,
      lineStyle: { width: 3, color: '#2563eb' },
      itemStyle: { color: '#2563eb' },
      areaStyle: { color: 'rgba(37, 99, 235, .10)' }
    }
  ]
}))
</script>
