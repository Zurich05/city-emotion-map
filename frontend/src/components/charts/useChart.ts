import * as echarts from 'echarts'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

export function useChart(optionGetter: () => echarts.EChartsOption) {
  const el = ref<HTMLDivElement>()
  let chart: echarts.ECharts | null = null
  const render = () => {
    if (!el.value) return
    chart ||= echarts.init(el.value)
    chart.setOption(optionGetter())
  }
  onMounted(() => {
    render()
    window.addEventListener('resize', render)
  })
  onBeforeUnmount(() => {
    window.removeEventListener('resize', render)
    chart?.dispose()
  })
  watch(optionGetter, render, { deep: true })
  return el
}
