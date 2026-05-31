<template>
  <div ref="mapEl" class="map"></div>
</template>

<script setup lang="ts">
import L from 'leaflet'
import 'leaflet.heat'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import type { EmotionPoint } from '../../api/emotion'

declare module 'leaflet' {
  function heatLayer(latlngs: Array<[number, number, number]>, options?: Record<string, unknown>): Layer
}

const props = defineProps<{ points: EmotionPoint[]; layer: string }>()
const mapEl = ref<HTMLDivElement>()
let map: L.Map | null = null
let group: L.LayerGroup | null = null
let heat: L.Layer | null = null

function color(point: EmotionPoint) {
  if (props.layer === '压力') return point.stress_score > .5 ? '#ef4444' : '#f97316'
  if (props.layer === '愉悦') return '#22c55e'
  if (props.layer === '愤怒') return '#dc2626'
  if (props.layer === '平静') return '#0ea5e9'
  if (point.sentiment_label === 'positive') return '#16a34a'
  if (point.sentiment_label === 'negative') return '#ef4444'
  return '#64748b'
}

function render() {
  if (!map) return
  group?.remove()
  if (heat) {
    heat.remove()
    heat = null
  }
  group = L.layerGroup().addTo(map)
  const located = props.points.filter(p => p.lat && p.lng)
  if (props.layer === '数据密度' || props.layer === '压力') {
    const heatPoints = located.map(point => [point.lat!, point.lng!, props.layer === '压力' ? Math.max(point.stress_score, .2) : .6] as [number, number, number])
    heat = L.heatLayer(heatPoints, { radius: 26, blur: 18, maxZoom: 14, gradient: { .2: '#38bdf8', .45: '#facc15', .75: '#fb923c', 1: '#ef4444' } }).addTo(map)
  }
  located.forEach(point => {
    L.circleMarker([point.lat!, point.lng!], {
      radius: props.layer === '数据密度' ? 8 : 7,
      color: '#fff',
      weight: 1,
      fillColor: color(point),
      fillOpacity: .78
    }).bindPopup(`<strong>${point.location_name || point.district || ''}</strong><br/>${point.text}<br/>压力 ${point.stress_score} 愉悦 ${point.joy_score}`).addTo(group!)
  })
}

onMounted(() => {
  if (!mapEl.value) return
  map = L.map(mapEl.value).setView([30.56, 114.32], 11)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap' }).addTo(map)
  render()
})
watch(() => [props.points, props.layer], render, { deep: true })
onBeforeUnmount(() => map?.remove())
</script>

<style scoped>
.map { width: 100%; height: calc(100vh - 178px); min-height: 520px; border-radius: 8px; overflow: hidden; }
</style>
