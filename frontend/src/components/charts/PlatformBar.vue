<template><div ref="el" class="chart"></div></template>
<script setup lang="ts">
import { useChart } from './useChart'
const props = defineProps<{ rows: Array<Record<string, any>> }>()
const el = useChart(() => ({
  tooltip: {},
  xAxis: {
    type: 'category',
    data: props.rows.map(i => platformName(i.platform)),
    axisLine: { lineStyle: { color: '#dbe5ef' } },
    axisLabel: { color: '#475569', fontSize: 14 }
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: '#edf2f7' } },
    axisLabel: { color: '#475569', fontSize: 14 }
  },
  series: [{
    type: 'bar',
    data: props.rows.map(i => i.count),
    barWidth: 28,
    itemStyle: {
      borderRadius: [5, 5, 0, 0],
      color: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [{ offset: 0, color: '#60a5fa' }, { offset: 1, color: '#2563eb' }]
      }
    }
  }]
}))

function platformName(platform: string) {
  return ({ weibo: '微博', xhs: '小红书', douyin: '抖音', mock: '模拟' } as Record<string, string>)[platform] || platform
}
</script>
