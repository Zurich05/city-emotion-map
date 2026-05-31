<template>
  <AppLayout title="情绪分析">
    <section class="page analysis">
      <div class="panel panel-pad"><h3 class="section-title">情绪占比</h3><EmotionPie :overview="overview" /></div>
      <div class="panel panel-pad"><h3 class="section-title">平台对比</h3><PlatformBar :rows="platformRows" /></div>
      <div class="panel panel-pad"><h3 class="section-title">时间趋势</h3><TrendLine :rows="timelineRows" /></div>
      <div class="panel panel-pad"><h3 class="section-title">区域排名</h3><DistrictRank :rows="rankRows" /></div>
    </section>
  </AppLayout>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchDistrictRank, fetchOverview, fetchPlatform, fetchTimeline } from '../api/statistics'
import DistrictRank from '../components/charts/DistrictRank.vue'
import EmotionPie from '../components/charts/EmotionPie.vue'
import PlatformBar from '../components/charts/PlatformBar.vue'
import TrendLine from '../components/charts/TrendLine.vue'
import AppLayout from '../components/layout/AppLayout.vue'
const overview = ref<any>({})
const platformRows = ref<any[]>([])
const timelineRows = ref<any[]>([])
const rankRows = ref<any[]>([])
onMounted(async () => {
  ;[overview.value, platformRows.value, timelineRows.value, rankRows.value] = await Promise.all([fetchOverview(), fetchPlatform(), fetchTimeline(), fetchDistrictRank()])
})
</script>
<style scoped>
.analysis { display: grid; grid-template-columns: repeat(2, minmax(280px, 1fr)); gap: 16px; }
@media (max-width: 900px) { .analysis { grid-template-columns: 1fr; } }
</style>
