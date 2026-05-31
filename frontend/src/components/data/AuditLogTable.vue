<template>
  <el-table :data="logs" height="300">
    <el-table-column prop="username" label="用户" width="100" />
    <el-table-column prop="method" label="方法" width="80" />
    <el-table-column prop="path" label="路径" />
    <el-table-column prop="status_code" label="状态" width="80" />
    <el-table-column prop="client_ip" label="IP" width="130" />
    <el-table-column prop="created_at" label="时间" width="180" />
  </el-table>
</template>

<script setup lang="ts">
defineProps<{ logs: Array<Record<string, any>> }>()
</script>
