<template><div ref="el" class="chart"></div></template>
<script setup lang="ts">
import { useChart } from './useChart'
const props = defineProps<{ overview: Record<string, number> }>()
const el = useChart(() => ({
  tooltip: { trigger: 'item' },
  series: [{ type: 'pie', radius: ['45%', '70%'], data: [
    { name: '积极', value: props.overview.positive_ratio || 0 },
    { name: '消极', value: props.overview.negative_ratio || 0 },
    { name: '中性', value: props.overview.neutral_ratio || 0 }
  ] }]
}))
</script>
