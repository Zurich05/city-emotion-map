<template>
  <article class="hotspot">
    <div class="head">
      <div>
        <strong>{{ areaName }}</strong>
        <span class="emotion-tag" :style="{ color: emotion.color }">{{ emotion.label }}</span>
      </div>
      <span class="risk-tag" :class="riskClass">{{ riskLabel }}</span>
    </div>
    <div class="keywords">
      <b v-for="word in keywords" :key="word">#{{ word }}</b>
    </div>
    <p>{{ mainReason }}</p>
    <p class="suggest">{{ suggestion }}</p>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ item: Record<string, any> }>()

const areaName = computed(() => props.item.location_name || props.item.district || '重点区域')
const riskLabel = computed(() => ({ high: '高风险', medium: '中风险', low: '低风险' }[props.item.risk_level as string] || '中风险'))
const riskClass = computed(() => props.item.risk_level === 'high' ? 'risk-high' : props.item.risk_level === 'low' ? 'risk-low' : 'risk-medium')
const mainReason = computed(() => props.item.main_reason || '区域情绪波动较明显，社交平台讨论热度上升。')
const suggestion = computed(() => props.item.suggestion || '建议加强舆情巡检，联动街道与公共服务部门进行快速响应。')
const keywords = computed(() => {
  const raw = props.item.keywords || props.item.keyword || mainReason.value
  if (Array.isArray(raw)) return raw.slice(0, 4)
  return String(raw).split(/[、，\s]+/).filter(Boolean).slice(0, 4)
})
const emotion = computed(() => {
  const level = props.item.risk_level
  if (level === 'high') return { label: '愤怒 / 压力', color: '#ef4444' }
  if (level === 'medium') return { label: '压力', color: '#f59e0b' }
  return { label: '平静', color: '#3b82f6' }
})
</script>

<style scoped>
.hotspot {
  padding: 16px;
  border-radius: 14px;
  border: 1px solid #e5edf5;
  background: #fff;
  margin-bottom: 12px;
}

.head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
}

strong {
  display: block;
  color: #0f172a;
  margin-bottom: 8px;
  font-size: 19px;
}

.keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 14px;
}

.keywords b {
  color: #2563eb;
  font-size: 14px;
  font-weight: 800;
  padding: 4px 9px;
  border-radius: 999px;
  background: #eff6ff;
}

p {
  margin: 13px 0 0;
  color: #334155;
  line-height: 1.65;
  font-size: 16px;
}

.suggest {
  color: #1e3a5f;
  padding: 12px;
  border-radius: 12px;
  background: #f8fbff;
}
</style>
