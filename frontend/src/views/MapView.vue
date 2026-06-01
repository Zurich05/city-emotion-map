<template>
  <AppLayout title="情绪地图">
    <section class="page map-page">
      <div class="page-head">
        <div>
          <h1>城市情绪地图</h1>
          <p>以情绪点位、风险等级、热点事件和治理建议呈现城市公共情绪空间分布。</p>
        </div>
        <div class="head-actions">
          <el-button @click="resetFilters">重置筛选</el-button>
          <el-button type="primary" @click="load">刷新数据</el-button>
        </div>
      </div>

      <div class="tech-toolbar">
        <el-select v-model="filter.platform" placeholder="平台来源" clearable style="width: 150px">
          <el-option label="微博" value="weibo" />
          <el-option label="小红书" value="xhs" />
          <el-option label="抖音" value="douyin" />
          <el-option label="模拟采集" value="mock" />
        </el-select>
        <el-input v-model="filter.district" placeholder="搜索区域或地点" clearable style="width: 190px" />
        <el-date-picker v-model="timeRange" type="daterange" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" style="width: 270px" />
        <el-select v-model="emotionType" placeholder="情绪类型" clearable style="width: 150px">
          <el-option label="积极" value="积极" />
          <el-option label="平静" value="平静" />
          <el-option label="压力" value="压力" />
          <el-option label="愤怒" value="愤怒" />
          <el-option label="忧虑" value="忧虑" />
        </el-select>
      </div>

      <div class="gis-layout">
        <aside class="layers panel panel-pad">
          <h3 class="section-title">情绪图层控制</h3>
          <LayerControl v-model="layer" v-model:heat="heatEnabled" />
          <div class="stat-box">
            <span>当前点位</span>
            <strong>{{ filteredPoints.length }}</strong>
          </div>
          <div class="risk-summary">
            <span class="risk-tag risk-low">低风险 {{ riskCounts.low }}</span>
            <span class="risk-tag risk-medium">中风险 {{ riskCounts.medium }}</span>
            <span class="risk-tag risk-high">高风险 {{ riskCounts.high }}</span>
          </div>
        </aside>

        <div class="map-column">
          <div class="panel map-panel">
            <EmotionMap
              :points="filteredPoints"
              :layer="emotionType || layer"
              :heat-enabled="heatEnabled"
              :selected-id="selectedPoint?.id"
              @select="selectPoint"
            />
          </div>
          <div class="timeline panel">
            <span>00:00</span>
            <i class="calm"></i>
            <b>今日情绪趋势</b>
            <i class="risk"></i>
            <span>24:00</span>
          </div>
        </div>

        <aside class="detail panel panel-pad">
          <h3 class="section-title">区域情绪画像</h3>
          <template v-if="selectedPoint">
            <div class="detail-head">
              <div>
                <strong>{{ selectedPoint.location_name || selectedPoint.district || '未知区域' }}</strong>
                <span>{{ selectedPoint.district || '城市区域' }}</span>
              </div>
              <span class="risk-tag" :class="riskClass(selectedPoint)">{{ riskLabel(selectedPoint) }}</span>
            </div>

            <div class="portrait-index">
              <small>情绪指数</small>
              <b>{{ emotionIndex(selectedPoint) }}</b>
              <em :style="{ color: emotionOf(selectedPoint).color }">{{ emotionOf(selectedPoint).label }}</em>
            </div>

            <section class="portrait-block">
              <h4>高频关键词</h4>
              <div class="keywords"><span v-for="word in keywords(selectedPoint)" :key="word">#{{ word }}</span></div>
            </section>

            <section class="portrait-block">
              <h4>平台来源占比</h4>
              <div class="source-row"><span>微博</span><i style="width: 42%"></i><b>42%</b></div>
              <div class="source-row"><span>小红书</span><i style="width: 31%"></i><b>31%</b></div>
              <div class="source-row"><span>抖音</span><i style="width: 27%"></i><b>27%</b></div>
            </section>

            <section class="portrait-block">
              <h4>热点事件摘要</h4>
              <p>{{ selectedPoint.text || '该区域社交平台讨论热度上升，需持续关注公共服务、交通出行与民生诉求相关情绪变化。' }}</p>
            </section>

            <section class="portrait-block">
              <h4>治理建议</h4>
              <ul>
                <li v-for="item in suggestionsFor(selectedPoint)" :key="item">{{ item }}</li>
              </ul>
            </section>
          </template>
          <template v-else>
            <p class="empty">点击地图点位后查看区域情绪画像。</p>
          </template>
        </aside>
      </div>
    </section>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { fetchEmotions, type EmotionPoint } from '../api/emotion'
import { fetchHotspots } from '../api/statistics'
import { useFilterStore } from '../stores/filter'
import AppLayout from '../components/layout/AppLayout.vue'
import EmotionMap from '../components/map/EmotionMap.vue'
import LayerControl from '../components/map/LayerControl.vue'

const filter = useFilterStore()
const points = ref<EmotionPoint[]>([])
const selectedPoint = ref<EmotionPoint | null>(null)
const layer = ref('综合情绪')
const heatEnabled = ref(false)
const emotionType = ref('')
const timeRange = ref('')

const filteredPoints = computed(() => {
  return points.value.filter(point => {
    const platformOk = !filter.platform || point.platform === filter.platform
    const districtOk = !filter.district || `${point.district || ''}${point.location_name || ''}`.includes(filter.district)
    const emotionOk = !emotionType.value || emotionOf(point).label === emotionType.value
    return platformOk && districtOk && emotionOk
  })
})

const riskCounts = computed(() => filteredPoints.value.reduce((acc, point) => {
  acc[riskLevel(point)] += 1
  return acc
}, { low: 0, medium: 0, high: 0 }))

function emotionOf(point: EmotionPoint) {
  const scores = [
    { label: '积极', color: '#10b981', value: point.joy_score || (point.sentiment_label === 'positive' ? point.sentiment_score : 0) },
    { label: '平静', color: '#3b82f6', value: point.calm_score || 0 },
    { label: '压力', color: '#f59e0b', value: point.stress_score || 0 },
    { label: '愤怒', color: '#ef4444', value: point.anger_score || 0 },
    { label: '忧虑', color: '#8b5cf6', value: point.sentiment_label === 'negative' ? Math.max(point.stress_score || 0, .55) : 0 }
  ]
  return scores.sort((a, b) => b.value - a.value)[0]
}

function emotionIndex(point: EmotionPoint) {
  return Math.round(Math.max(point.sentiment_score || 0, point.stress_score || 0, point.joy_score || 0, .3) * 100)
}

function riskLevel(point: EmotionPoint): 'low' | 'medium' | 'high' {
  if ((point.anger_score || 0) > .55 || (point.stress_score || 0) > .72) return 'high'
  if ((point.stress_score || 0) > .45 || point.sentiment_label === 'negative') return 'medium'
  return 'low'
}

function riskClass(point: EmotionPoint) { return `risk-${riskLevel(point)}` }
function riskLabel(point: EmotionPoint) { return ({ low: '低风险', medium: '中风险', high: '高风险' } as Record<string, string>)[riskLevel(point)] }
function keywords(point: EmotionPoint) { return String(point.text || '城市 情绪 治理 服务 热点').split(/[、，\s]+/).filter(Boolean).slice(0, 5) }

function suggestionsFor(point: EmotionPoint) {
  const risk = riskLevel(point)
  if (risk === 'high') return ['核查负向情绪诱因，联动属地部门快速响应。', '加强重点时段舆情巡检，形成事件闭环处置记录。', '发布权威说明，降低谣言扩散与二次情绪风险。']
  if (risk === 'medium') return ['持续跟踪关键词变化，识别情绪升温的具体场景。', '优化公共服务沟通频次，在高峰时段加强解释引导。', '将该区域纳入次日重点巡检清单。']
  return ['保持常态化监测，沉淀正向反馈案例。', '关注趋势异常波动，避免低风险转为聚集性问题。']
}

function selectPoint(point: EmotionPoint) { selectedPoint.value = point }

function resetFilters() {
  filter.platform = ''
  filter.district = ''
  emotionType.value = ''
  timeRange.value = ''
  heatEnabled.value = false
  layer.value = '综合情绪'
}

async function load() {
  const [emotionRows] = await Promise.all([fetchEmotions(), fetchHotspots()])
  points.value = emotionRows
  selectedPoint.value = points.value[0] || null
}

watch(filteredPoints, rows => {
  if (!rows.some(point => point.id === selectedPoint.value?.id)) selectedPoint.value = rows[0] || null
})

onMounted(load)
</script>

<style scoped>
.map-page {
  display: grid;
  gap: 20px;
}

.page-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 20px;
}

.page-head h1 {
  margin: 0 0 8px;
  font-size: 36px;
  color: #0f172a;
}

.page-head p {
  margin: 0;
  color: #64748b;
  font-size: 17px;
}

.head-actions {
  display: flex;
  gap: 10px;
}

.gis-layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr) 340px;
  gap: 20px;
  align-items: start;
}

.map-panel {
  padding: 8px;
}

.stat-box {
  margin-top: 20px;
  padding: 16px;
  border-radius: 14px;
  background: #f8fbff;
  border: 1px solid #e2eaf4;
}

.stat-box span {
  color: #64748b;
  font-size: 15px;
}

.stat-box strong {
  display: block;
  margin-top: 4px;
  color: #0f172a;
  font-size: 36px;
}

.risk-summary {
  display: grid;
  gap: 8px;
  margin-top: 14px;
}

.timeline {
  height: 58px;
  margin-top: 14px;
  padding: 0 18px;
  display: grid;
  grid-template-columns: auto 1fr auto 1fr auto;
  gap: 12px;
  align-items: center;
  color: #64748b;
  font-size: 14px;
}

.timeline i {
  height: 7px;
  border-radius: 999px;
}

.timeline .calm { background: linear-gradient(90deg, #3b82f6, #10b981); }
.timeline .risk { background: linear-gradient(90deg, #f59e0b, #ef4444, #8b5cf6); }

.timeline b {
  color: #0f172a;
  font-size: 15px;
}

.detail {
  max-height: calc(100vh - 148px);
  overflow: auto;
}

.detail-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.detail-head strong {
  display: block;
  color: #0f172a;
  font-size: 22px;
  margin-bottom: 4px;
}

.detail-head span,
.empty {
  color: #64748b;
  font-size: 15px;
}

.portrait-index {
  margin: 20px 0;
  padding: 18px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 6px 12px;
  align-items: end;
  border-radius: 16px;
  background: linear-gradient(135deg, #f8fbff, #eef6ff);
  border: 1px solid #e2eaf4;
}

.portrait-index small {
  color: #64748b;
  font-size: 15px;
}

.portrait-index b {
  grid-row: span 2;
  color: #0f172a;
  font-size: 46px;
  line-height: 1;
}

.portrait-index em {
  font-style: normal;
  font-weight: 900;
  font-size: 17px;
}

.portrait-block {
  padding-top: 16px;
  border-top: 1px solid #e6eef7;
}

.portrait-block h4 {
  margin: 0 0 10px;
  color: #475569;
  font-size: 15px;
  font-weight: 900;
}

.portrait-block p,
.portrait-block li {
  color: #334155;
  font-size: 16px;
  line-height: 1.75;
}

.portrait-block ul {
  margin: 0;
  padding-left: 18px;
}

.keywords span {
  display: inline-block;
  margin: 0 7px 7px 0;
  padding: 5px 10px;
  color: #2563eb;
  border-radius: 999px;
  background: #eff6ff;
  font-weight: 800;
  font-size: 14px;
}

.source-row {
  display: grid;
  grid-template-columns: 58px 1fr 38px;
  gap: 10px;
  align-items: center;
  margin: 9px 0;
  color: #475569;
  font-size: 14px;
}

.source-row i {
  height: 7px;
  border-radius: 999px;
  background: #2563eb;
}

.source-row b {
  color: #0f172a;
}

@media (max-width: 1320px) {
  .gis-layout { grid-template-columns: 220px minmax(0, 1fr); }
  .detail { grid-column: 1 / -1; max-height: none; }
}

@media (max-width: 860px) {
  .gis-layout { grid-template-columns: 1fr; }
  .page-head { align-items: flex-start; flex-direction: column; }
}
</style>
