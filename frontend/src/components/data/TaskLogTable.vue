<template>
  <el-table :data="logs" height="300">
    <el-table-column prop="task_type" label="任务" width="120" />
    <el-table-column prop="platform" label="平台" width="90" />
    <el-table-column prop="total_count" label="总数" width="80" />
    <el-table-column prop="success_count" label="成功" width="80" />
    <el-table-column prop="failed_count" label="失败" width="80" />
    <el-table-column prop="status" label="状态" width="90" />
    <el-table-column prop="start_time" label="开始时间" />
  </el-table>
</template>

<script setup lang="ts">
defineProps<{ logs: Array<Record<string, any>> }>()
</script>
