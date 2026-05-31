<template>
  <article class="hotspot panel panel-pad">
    <div class="head">
      <strong>{{ item.district }} · {{ item.location_name }}</strong>
      <el-tag :type="tagType" size="small">{{ riskLabel }}</el-tag>
    </div>
    <p>{{ item.main_reason }}</p>
    <p class="suggest">{{ item.suggestion }}</p>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ item: Record<string, any> }>()
const tagType = computed(() => props.item.risk_level === 'high' ? 'danger' : props.item.risk_level === 'medium' ? 'warning' : 'success')
const riskLabel = computed(() => ({ high: '高风险', medium: '中风险', low: '低风险' }[props.item.risk_level as string] || props.item.risk_level))
</script>

<style scoped>
.hotspot { margin-bottom: 12px; }
.head { display: flex; justify-content: space-between; gap: 8px; }
p { margin: 10px 0 0; color: #475569; line-height: 1.6; }
.suggest { color: #1d4ed8; }
</style>
