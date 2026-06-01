<template>
  <div class="rank-list">
    <div v-for="(row, index) in rows" :key="row.district || index" class="rank-row">
      <b>{{ index + 1 }}</b>
      <span>{{ row.district || '未知区域' }}</span>
      <div class="bar"><i :style="{ width: widthOf(row) }"></i></div>
      <em>{{ riskLabel(row.risk_level) }}</em>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ rows: Array<Record<string, any>> }>()

function widthOf(row: Record<string, any>) {
  const score = Number(row.avg_stress_score || row.negative_ratio || row.total_count || 0)
  return `${Math.max(14, Math.min(100, Math.round(score * 100)))}%`
}

function riskLabel(level: string) {
  return ({ high: '高风险', medium: '中风险', low: '低风险' } as Record<string, string>)[level] || level || '观察'
}
</script>

<style scoped>
.rank-list {
  height: 320px;
  overflow: auto;
  display: grid;
  gap: 10px;
  align-content: start;
}

.rank-row {
  display: grid;
  grid-template-columns: 30px minmax(70px, 110px) 1fr 64px;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border: 1px solid rgba(50,230,255,.16);
  background: rgba(255,255,255,.035);
  border-radius: 8px;
}

b {
  color: #2563eb;
}

span {
  color: #334155;
  font-weight: 700;
  font-size: 15px;
}

.bar {
  height: 8px;
  border-radius: 999px;
  background: #edf2f7;
  overflow: hidden;
}

.bar i {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #4d8fd8, #9a78c7, #d99a4e);
}

em {
  color: #b45309;
  font-size: 14px;
  font-style: normal;
  text-align: right;
}
</style>
