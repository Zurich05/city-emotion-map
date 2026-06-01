<template>
  <AppLayout title="报告中心">
    <section class="page report-grid">
      <div class="panel panel-pad">
        <div class="report-head">
          <h3 class="section-title">治理摘要报告</h3>
          <div class="actions">
            <el-button @click="copy">复制</el-button>
            <el-button type="primary" @click="downloadText('txt')">导出 TXT</el-button>
            <el-button @click="downloadNative('pdf')">导出 PDF</el-button>
            <el-button @click="downloadNative('docx')">导出 DOCX</el-button>
          </div>
        </div>
        <pre>{{ report.summary || fallbackSummary }}</pre>
      </div>
      <aside>
        <div class="panel panel-pad report-stat">
          <span>报告状态</span>
          <strong>已生成</strong>
          <p>基于热点区域、负向情绪、压力趋势自动汇总。</p>
        </div>
        <HotspotCard v-for="item in report.hotspots || []" :key="item.location_name" :item="item" />
      </aside>
    </section>
  </AppLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { downloadReport, fetchReport } from '../api/statistics'
import HotspotCard from '../components/cards/HotspotCard.vue'
import AppLayout from '../components/layout/AppLayout.vue'

const report = ref<any>({ summary: '', hotspots: [] })
const fallbackSummary = '城市情绪总体保持平稳，局部区域出现压力与负向讨论升温。建议围绕交通通勤、公共服务、夜间安全等关键词开展分级响应，并持续跟踪热点事件扩散。'

async function copy() { await navigator.clipboard.writeText(report.value.summary || fallbackSummary) }
function downloadText(type: 'txt') {
  const blob = new Blob([report.value.summary || fallbackSummary], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = `city-emotion-report.${type}`
  anchor.click()
  URL.revokeObjectURL(url)
}
async function downloadNative(format: 'pdf' | 'docx') { await downloadReport(format) }
onMounted(async () => { report.value = await fetchReport() })
</script>

<style scoped>
.report-grid {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 22px;
}
.report-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}
pre {
  white-space: pre-wrap;
  line-height: 1.9;
  color: #334155;
  font-family: inherit;
  font-size: 15px;
  padding: 18px;
  border: 1px solid #e2eaf4;
  border-radius: 14px;
  background: #f8fbff;
}
.report-stat { margin-bottom: 14px; }
.report-stat span { color: #64748b; }
.report-stat strong {
  display: block;
  margin: 8px 0;
  color: #10b981;
  font-size: 30px;
}
.report-stat p { color: #64748b; line-height: 1.7; margin: 0; }
@media (max-width: 980px) {
  .report-grid { grid-template-columns: 1fr; }
}
</style>
