<template><div ref="el" class="chart"></div></template>
<script setup lang="ts">
import { useChart } from './useChart'
const props = defineProps<{ overview: Record<string, number> }>()
const el = useChart(() => ({
  tooltip: { trigger: 'item' },
  legend: { bottom: 0, itemGap: 18, textStyle: { color: '#334155', fontSize: 15, fontWeight: 600 } },
  series: [{
    type: 'pie',
    radius: ['48%', '72%'],
    center: ['50%', '45%'],
    roseType: 'radius',
    label: { color: '#334155', fontSize: 16, fontWeight: 700 },
    labelLine: { lineStyle: { color: '#64748b' } },
    data: [
      { name: '积极', value: props.overview.positive_ratio || 0, itemStyle: { color: '#4fb783' } },
      { name: '压力/消极', value: props.overview.negative_ratio || 0, itemStyle: { color: '#d95f68' } },
      { name: '平静', value: props.overview.neutral_ratio || 0, itemStyle: { color: '#4d8fd8' } }
    ]
  }]
}))
</script>
