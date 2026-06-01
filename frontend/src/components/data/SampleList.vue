<template>
  <el-table :data="points" height="360">
    <el-table-column prop="platform" label="平台" width="90" />
    <el-table-column prop="district" label="区域" width="110" />
    <el-table-column prop="location_name" label="地点" width="130" />
    <el-table-column prop="sentiment_label" label="情绪" width="90" />
    <el-table-column prop="text" label="文本" />
  </el-table>
</template>

<script setup lang="ts">
import type { EmotionPoint } from '../../api/emotion'
defineProps<{ points: EmotionPoint[] }>()
</script>
