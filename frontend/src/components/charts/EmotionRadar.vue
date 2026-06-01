<template><div ref="el" class="chart"></div></template>
<script setup lang="ts">
import { useChart } from './useChart'
const props = defineProps<{ overview: Record<string, number> }>()
const el = useChart(() => ({
  radar: {
    indicator: [
      { name: '积极', max: 1 },
      { name: '平静', max: 1 },
      { name: '压力', max: 1 },
      { name: '愤怒', max: 1 },
      { name: '忧虑', max: 1 }
    ],
    axisName: { color: '#334155', fontSize: 15, fontWeight: 700 },
    splitLine: { lineStyle: { color: '#dbe5ef' } },
    splitArea: { areaStyle: { color: ['#f8fbff', '#eef5ff'] } },
    axisLine: { lineStyle: { color: '#dbe5ef' } }
  },
  series: [{
    type: 'radar',
    data: [{
      value: [
        props.overview.positive_ratio || .42,
        props.overview.neutral_ratio || .35,
        props.overview.avg_stress_score || .3,
        Math.max((props.overview.negative_ratio || 0) * .82, .18),
        props.overview.negative_ratio || .24
      ],
      name: '城市情绪画像',
      areaStyle: { color: 'rgba(37, 99, 235, .12)' },
      lineStyle: { color: '#2563eb', width: 2 },
      itemStyle: { color: '#2563eb' }
    }]
  }]
}))
</script>
