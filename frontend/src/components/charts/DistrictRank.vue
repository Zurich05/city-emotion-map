<template>
  <el-table :data="rows" height="320">
    <el-table-column prop="district" label="区域" />
    <el-table-column prop="total_count" label="样本" width="80" />
    <el-table-column prop="negative_ratio" label="负面比" width="90" />
    <el-table-column prop="avg_stress_score" label="压力" width="90" />
    <el-table-column prop="risk_level" label="风险" width="90" />
  </el-table>
</template>
<script setup lang="ts">
defineProps<{ rows: Array<Record<string, any>> }>()
</script>
