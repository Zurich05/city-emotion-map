<template>
  <div class="metric panel panel-pad">
    <span>{{ label }}</span>
    <strong>{{ value }}</strong>
    <small>{{ hint }}</small>
  </div>
</template>

<script setup lang="ts">
defineProps<{ label: string; value: string | number; hint?: string }>()
</script>

<style scoped>
.metric { min-height: 112px; display: flex; flex-direction: column; justify-content: space-between; }
span { color: #64748b; font-size: 13px; }
strong { font-size: 28px; line-height: 1; }
small { color: #7c8aa0; }
</style>
