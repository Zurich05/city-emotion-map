<template>
  <header class="top panel">
    <strong>{{ title }}</strong>
    <div class="filters">
      <el-select v-model="filter.platform" placeholder="平台" clearable size="small" style="width:120px">
        <el-option label="微博" value="weibo" />
        <el-option label="小红书" value="xhs" />
        <el-option label="抖音" value="douyin" />
        <el-option label="模拟" value="mock" />
      </el-select>
      <el-input v-model="filter.district" placeholder="区域" clearable size="small" style="width:140px" />
    </div>
  </header>
</template>

<script setup lang="ts">
import { useFilterStore } from '../../stores/filter'
defineProps<{ title: string }>()
const filter = useFilterStore()
</script>

<style scoped>
.top { height: 64px; margin: 16px 22px 0; padding: 0 18px; display: flex; align-items: center; justify-content: space-between; }
.filters { display: flex; gap: 10px; }
</style>
