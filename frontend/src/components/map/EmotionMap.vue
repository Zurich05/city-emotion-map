<template>
  <div class="map-shell">
    <div ref="mapEl" class="map"></div>
    <div class="legend">
      <span v-for="item in legend" :key="item.label">
        <i :style="{ background: item.color }"></i>{{ item.label }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import L from 'leaflet'
import 'leaflet.heat'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import type { EmotionPoint } from '../../api/emotion'

declare module 'leaflet' {
  function heatLayer(latlngs: Array<[number, number, number]>, options?: Record<string, unknown>): Layer
}

const props = defineProps<{ points: EmotionPoint[]; layer: string; heatEnabled?: boolean; selectedId?: number }>()
const emit = defineEmits<{ select: [point: EmotionPoint] }>()
const mapEl = ref<HTMLDivElement>()
let map: L.Map | null = null
let group: L.LayerGroup | null = null
let heat: L.Layer | null = null

const legend = [
  { label: '积极', color: '#10b981' },
  { label: '平静', color: '#3b82f6' },
  { label: '压力', color: '#f59e0b' },
  { label: '愤怒', color: '#ef4444' },
  { label: '忧虑', color: '#8b5cf6' }
]

function emotionOf(point: EmotionPoint) {
  const scores = [
    { key: '积极', label: '积极', color: '#10b981', value: point.joy_score || (point.sentiment_label === 'positive' ? point.sentiment_score : 0) },
    { key: '平静', label: '平静', color: '#3b82f6', value: point.calm_score || 0 },
    { key: '压力', label: '压力', color: '#f59e0b', value: point.stress_score || 0 },
    { key: '愤怒', label: '愤怒', color: '#ef4444', value: point.anger_score || 0 },
    { key: '忧虑', label: '忧虑', color: '#8b5cf6', value: point.sentiment_label === 'negative' ? Math.max(point.stress_score || 0, .55) : 0 }
  ]
  if (props.layer !== '综合情绪' && props.layer !== '数据密度') {
    return scores.find(item => item.key === props.layer) || scores[0]
  }
  return scores.sort((a, b) => b.value - a.value)[0] || scores[0]
}

function platformName(platform: string) {
  return ({ weibo: '微博', xhs: '小红书', douyin: '抖音', mock: '模拟采集' } as Record<string, string>)[platform] || platform || '社交平台'
}

function tooltip(point: EmotionPoint) {
  const emotion = emotionOf(point)
  const area = point.location_name || point.district || '未知区域'
  const index = Math.round(Math.max(point.sentiment_score || 0, point.stress_score || 0, point.joy_score || 0, .3) * 100)
  return `<strong>${area}</strong><br/>${emotion.label} · 情绪指数 ${index}<br/>${platformName(point.platform)}`
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

  if (props.heatEnabled || props.layer === '数据密度') {
    const heatPoints = located.map(point => {
      const intensity = props.layer === '数据密度' ? .38 : Math.max(point.stress_score || 0, point.anger_score || 0, point.joy_score || 0, .22)
      return [point.lat!, point.lng!, intensity] as [number, number, number]
    })
    heat = L.heatLayer(heatPoints, {
      radius: 24,
      blur: 18,
      maxZoom: 14,
      minOpacity: .22,
      gradient: { .18: '#3b82f6', .42: '#10b981', .68: '#f59e0b', .86: '#ef4444', 1: '#8b5cf6' }
    }).addTo(map)
  }

  located.forEach(point => {
    const emotion = emotionOf(point)
    const selected = props.selectedId === point.id
    const marker = L.circleMarker([point.lat!, point.lng!], {
      radius: selected ? 10 : 8,
      color: 'rgba(255,255,255,.96)',
      weight: selected ? 3 : 2,
      opacity: 1,
      fillColor: emotion.color,
      fillOpacity: .95,
      className: selected ? 'selected-marker' : ''
    })
      .bindTooltip(tooltip(point), { className: 'emotion-tooltip', direction: 'top', offset: [0, -8] })
      .on('click', () => emit('select', point))
      .addTo(group!)
    marker.on('mouseover', () => marker.setStyle({ radius: selected ? 11 : 9 }))
    marker.on('mouseout', () => marker.setStyle({ radius: selected ? 10 : 8 }))
  })
}

onMounted(() => {
  if (!mapEl.value) return
  map = L.map(mapEl.value, { zoomControl: false }).setView([30.56, 114.32], 11)
  L.control.zoom({ position: 'bottomleft' }).addTo(map)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO',
    maxZoom: 19
  }).addTo(map)
  render()
})

watch(() => [props.points, props.layer, props.heatEnabled, props.selectedId], render, { deep: true })
onBeforeUnmount(() => map?.remove())
</script>

<style scoped>
.map-shell {
  position: relative;
  min-height: 640px;
  border-radius: 16px;
  overflow: hidden;
  background: #e7eef7;
}

.map {
  width: 100%;
  height: calc(100vh - 250px);
  min-height: 640px;
  filter: saturate(.88) contrast(.96) hue-rotate(178deg) brightness(1.02);
}

.legend {
  position: absolute;
  right: 16px;
  bottom: 16px;
  z-index: 402;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 10px 12px;
  border: 1px solid #d7e1ec;
  border-radius: 14px;
  background: rgba(255,255,255,.94);
  box-shadow: 0 10px 24px rgba(15, 23, 42, .12);
}

.legend span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #334155;
  font-size: 14px;
  font-weight: 750;
}

.legend i {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

:global(.leaflet-container) {
  background: #e7eef7;
}

:global(.leaflet-control-zoom a) {
  color: #1f3347;
  border-color: #d7e1ec;
}

:global(.selected-marker) {
  filter: drop-shadow(0 3px 8px rgba(15, 23, 42, .25));
}

:global(.emotion-tooltip) {
  background: #fff;
  color: #334155;
  border: 1px solid #d7e1ec;
  box-shadow: 0 10px 24px rgba(15, 23, 42, .14);
  border-radius: 10px;
  font-size: 14px;
}

:global(.emotion-tooltip::before) {
  border-top-color: #fff;
}

@media (max-width: 760px) {
  .map-shell,
  .map { min-height: 520px; }
}
</style>
