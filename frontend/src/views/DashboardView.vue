<template>
  <AppLayout title="城市情绪分析工作台">
    <section class="page dashboard">
      <div class="overview panel panel-pad">
        <div class="overview-main">
          <span>城市情绪总览</span>
          <h1>城市情绪分析工作台</h1>
          <p>汇聚社交媒体文本、空间位置、情绪类型和热点事件，形成可用于公共治理的城市情绪运行画像。</p>
        </div>
        <div class="overview-index">
          <small>综合情绪指数</small>
          <strong>{{ emotionIndex }}</strong>
          <em>整体状态：平稳</em>
        </div>
        <div class="overview-meta">
          <b>主要热点区域</b>
          <span>{{ hotspots[0]?.location_name || hotspots[0]?.district || '暂无热点' }}</span>
          <b>主要情绪</b>
          <span>平静 / 压力</span>
        </div>
      </div>

      <div class="grid metrics">
        <MetricCard label="今日采集量" :value="overview.today_count" trend="+12%" hint="来自微博、小红书、抖音等平台" />
        <MetricCard label="高风险区域" :value="overview.high_risk_count" trend="待处置" hint="需优先关注的空间单元" />
        <MetricCard label="热点事件" :value="hotspots.length" trend="实时" hint="区域讨论热度聚合结果" />
        <MetricCard label="治理建议数量" :value="hotspots.length || 0" trend="自动生成" hint="面向区域情绪风险的处置建议" />
      </div>

      <div class="chart-row">
        <div class="panel panel-pad wide">
          <div class="title-row">
            <h3 class="section-title">情绪趋势</h3>
            <span class="subtle">近 24 小时</span>
          </div>
          <TrendLine :rows="timelineRows" />
        </div>
        <div class="panel panel-pad">
          <div class="title-row">
            <h3 class="section-title">情绪分布</h3>
            <span class="subtle">综合占比</span>
          </div>
          <EmotionRadar :overview="overview" />
        </div>
      </div>

      <div class="workbench-grid">
        <div class="panel panel-pad">
          <h3 class="section-title">热点事件列表</h3>
          <HotspotCard v-for="item in hotspots.slice(0, 3)" :key="item.location_name || item.district" :item="item" />
          <p v-if="!hotspots.length" class="empty">暂无热点事件。</p>
        </div>
        <div class="panel panel-pad">
          <h3 class="section-title">区域排行</h3>
          <DistrictRank :rows="rankRows" />
        </div>
        <div class="panel panel-pad suggestions">
          <h3 class="section-title">治理建议</h3>
          <div v-for="item in suggestionCards" :key="item.title" class="suggestion-card">
            <strong>{{ item.title }}</strong>
            <p>{{ item.text }}</p>
          </div>
        </div>
      </div>
    </section>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import MetricCard from '../components/cards/MetricCard.vue'
import HotspotCard from '../components/cards/HotspotCard.vue'
import DistrictRank from '../components/charts/DistrictRank.vue'
import EmotionRadar from '../components/charts/EmotionRadar.vue'
import TrendLine from '../components/charts/TrendLine.vue'
import AppLayout from '../components/layout/AppLayout.vue'
import { fetchDistrictRank, fetchHotspots, fetchOverview, fetchPlatform, fetchTimeline, type Overview } from '../api/statistics'

const overview = ref<Overview>({ total_count: 0, today_count: 0, positive_ratio: 0, negative_ratio: 0, neutral_ratio: 0, avg_sentiment_score: 0, avg_stress_score: 0, avg_joy_score: 0, high_risk_count: 0 })
const platformRows = ref<any[]>([])
const timelineRows = ref<any[]>([])
const rankRows = ref<any[]>([])
const hotspots = ref<any[]>([])
const emotionIndex = computed(() => Math.max(0, Math.min(100, Math.round(((overview.value.avg_sentiment_score || .5) * 62 + (overview.value.positive_ratio || 0) * 28 + (1 - (overview.value.avg_stress_score || 0)) * 10)))))
const suggestionCards = computed(() => [
  { title: '高风险区域优先响应', text: `${overview.value.high_risk_count || 0} 个区域建议纳入今日重点巡检，形成责任部门与处置时限。` },
  { title: '热点事件闭环跟踪', text: `当前识别 ${hotspots.value.length || 0} 个热点事件，建议按风险等级建立跟踪台账。` },
  { title: '公共服务沟通优化', text: '对压力和忧虑情绪集中的区域，建议提高政策解释、交通引导与民生服务反馈频次。' }
])

onMounted(async () => {
  ;[overview.value, platformRows.value, timelineRows.value, rankRows.value, hotspots.value] = await Promise.all([
    fetchOverview(),
    fetchPlatform(),
    fetchTimeline(),
    fetchDistrictRank(),
    fetchHotspots()
  ])
})
</script>

<style scoped>
.dashboard {
  display: grid;
  gap: 22px;
}

.overview {
  min-height: 220px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 210px 250px;
  gap: 26px;
  align-items: center;
  background:
    linear-gradient(90deg, rgba(239,246,255,.92), rgba(255,255,255,.98)),
    #fff;
}

.overview-main span {
  color: #2563eb;
  font-size: 15px;
  font-weight: 900;
}

.overview h1 {
  margin: 12px 0 12px;
  color: #0f172a;
  font-size: clamp(34px, 4vw, 48px);
}

.overview p {
  max-width: 720px;
  margin: 0;
  color: #64748b;
  font-size: 17px;
  line-height: 1.75;
}

.overview-index,
.overview-meta {
  padding: 18px;
  border-radius: 16px;
  background: #fff;
  border: 1px solid #e2eaf4;
}

.overview-index small,
.overview-index em,
.overview-meta b {
  display: block;
  color: #64748b;
  font-size: 14px;
  font-style: normal;
}

.overview-index strong {
  display: block;
  margin: 8px 0;
  color: #10b981;
  font-size: 54px;
  line-height: 1;
}

.overview-meta b {
  margin-top: 12px;
  font-weight: 800;
}

.overview-meta b:first-child {
  margin-top: 0;
}

.overview-meta span {
  display: block;
  margin-top: 5px;
  color: #0f172a;
  font-size: 16px;
  font-weight: 900;
}

.chart-row {
  display: grid;
  grid-template-columns: minmax(0, 1.45fr) minmax(320px, .85fr);
  gap: 22px;
}

.workbench-grid {
  display: grid;
  grid-template-columns: minmax(320px, 1.1fr) minmax(300px, .9fr) minmax(300px, .9fr);
  gap: 22px;
}

.empty {
  color: #64748b;
}

.suggestion-card {
  padding: 16px;
  border: 1px solid #e5edf5;
  border-radius: 14px;
  background: #f8fbff;
  margin-bottom: 12px;
}

.suggestion-card strong {
  display: block;
  color: #172033;
  font-size: 16px;
  margin-bottom: 8px;
}

.suggestion-card p {
  margin: 0;
  color: #475569;
  font-size: 14px;
  line-height: 1.65;
}

@media (max-width: 1280px) {
  .overview { grid-template-columns: 1fr 210px; }
  .overview-meta { grid-column: 1 / -1; }
  .workbench-grid { grid-template-columns: 1fr; }
}

@media (max-width: 820px) {
  .overview,
  .chart-row { grid-template-columns: 1fr; }
}
</style>
