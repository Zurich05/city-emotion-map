<template>
  <AppLayout title="城市情绪仪表盘">
    <section class="page grid">
      <div class="grid metrics">
        <MetricCard label="总样本" :value="overview.total_count" />
        <MetricCard label="今日新增" :value="overview.today_count" />
        <MetricCard label="积极比例" :value="percent(overview.positive_ratio)" />
        <MetricCard label="消极比例" :value="percent(overview.negative_ratio)" />
        <MetricCard label="平均压力" :value="overview.avg_stress_score" />
        <MetricCard label="高风险区域" :value="overview.high_risk_count" />
      </div>
      <div class="dashboard-grid">
        <div class="panel panel-pad"><h3 class="section-title">平台来源</h3><PlatformBar :rows="platformRows" /></div>
        <div class="panel panel-pad"><h3 class="section-title">情绪趋势</h3><TrendLine :rows="timelineRows" /></div>
        <div class="panel panel-pad"><h3 class="section-title">热点区域</h3><HotspotCard v-for="item in hotspots" :key="item.location_name" :item="item" /></div>
      </div>
    </section>
  </AppLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import MetricCard from '../components/cards/MetricCard.vue'
import HotspotCard from '../components/cards/HotspotCard.vue'
import PlatformBar from '../components/charts/PlatformBar.vue'
import TrendLine from '../components/charts/TrendLine.vue'
import AppLayout from '../components/layout/AppLayout.vue'
import { fetchHotspots, fetchOverview, fetchPlatform, fetchTimeline, type Overview } from '../api/statistics'
const overview = ref<Overview>({ total_count: 0, today_count: 0, positive_ratio: 0, negative_ratio: 0, neutral_ratio: 0, avg_sentiment_score: 0, avg_stress_score: 0, avg_joy_score: 0, high_risk_count: 0 })
const platformRows = ref<any[]>([])
const timelineRows = ref<any[]>([])
const hotspots = ref<any[]>([])
const percent = (value: number) => `${Math.round((value || 0) * 100)}%`
onMounted(async () => {
  ;[overview.value, platformRows.value, timelineRows.value, hotspots.value] = await Promise.all([fetchOverview(), fetchPlatform(), fetchTimeline(), fetchHotspots()])
})
</script>

<style scoped>
.dashboard-grid { display: grid; grid-template-columns: 1fr 1fr 360px; gap: 16px; }
@media (max-width: 1200px) { .dashboard-grid { grid-template-columns: 1fr; } }
</style>
