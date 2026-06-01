<template>
  <div class="metric panel panel-pad">
    <div class="metric-top">
      <span>{{ label }}</span>
      <i>{{ trend }}</i>
    </div>
    <strong>{{ value }}</strong>
    <small>{{ hint }}</small>
  </div>
</template>

<script setup lang="ts">
defineProps<{ label: string; value: string | number; hint?: string; trend?: string }>()
</script>

<style scoped>
.metric {
  min-height: 140px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.metric-top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

span {
  display: block;
  color: #64748b;
  font-size: 17px;
  font-weight: 800;
}

i {
  font-style: normal;
  color: #2563eb;
  background: #eff6ff;
  border-radius: 999px;
  padding: 4px 8px;
  font-size: 13px;
  font-weight: 850;
}

strong {
  display: block;
  margin-top: 14px;
  color: #172033;
  font-size: 44px;
  line-height: 1;
}

small {
  color: #64748b;
  font-size: 15px;
  line-height: 1.5;
}
</style>
