<template>
  <AppLayout title="情绪分析">
    <section class="page analysis-page">
      <div class="page-head">
        <h1>情绪分析</h1>
        <p>从时间、平台、区域和关键词维度分析城市情绪变化。</p>
      </div>
      <div class="analysis">
        <div class="panel panel-pad"><h3 class="section-title">情绪占比</h3><EmotionPie :overview="overview" /></div>
        <div class="panel panel-pad"><h3 class="section-title">平台对比</h3><PlatformBar :rows="platformRows" /></div>
        <div class="panel panel-pad wide"><h3 class="section-title">时间趋势</h3><TrendLine :rows="timelineRows" /></div>
        <div class="panel panel-pad"><h3 class="section-title">区域情绪排名</h3><DistrictRank :rows="rankRows" /></div>
        <div class="panel panel-pad insight">
          <h3 class="section-title">分析结论</h3>
          <p>当前城市情绪呈现空间分异：交通枢纽与商业密集区更容易出现压力信号，公园、文旅与社区服务相关区域保持较强正向反馈。</p>
          <p>建议结合时间趋势与区域排名，对高压力片区进行分级巡检，并跟踪舆情关键词的突增变化。</p>
        </div>
      </div>
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
.analysis-page { display: grid; gap: 20px; }
.page-head h1 { margin: 0 0 8px; font-size: 36px; color: #0f172a; }
.page-head p { margin: 0; color: #64748b; font-size: 17px; }
.analysis {
  display: grid;
  grid-template-columns: repeat(2, minmax(280px, 1fr));
  gap: 22px;
}
.wide { grid-column: span 2; }
.insight p {
  color: #334155;
  font-size: 16px;
  line-height: 1.8;
  margin: 0 0 14px;
}
@media (max-width: 900px) {
  .analysis { grid-template-columns: 1fr; }
  .wide { grid-column: auto; }
}
</style>
