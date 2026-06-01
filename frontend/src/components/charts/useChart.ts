import * as echarts from 'echarts'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

export function useChart(optionGetter: () => echarts.EChartsOption) {
  const el = ref<HTMLDivElement>()
  let chart: echarts.ECharts | null = null
  const render = () => {
    if (!el.value) return
    chart ||= echarts.init(el.value)
    chart.setOption({
      backgroundColor: 'transparent',
      textStyle: { color: '#334155', fontSize: 15 },
      grid: { left: 54, right: 26, top: 42, bottom: 46 },
      tooltip: {
        backgroundColor: '#ffffff',
        borderColor: '#dbe5ef',
        textStyle: { color: '#334155', fontSize: 15 }
      },
      ...optionGetter()
    })
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
