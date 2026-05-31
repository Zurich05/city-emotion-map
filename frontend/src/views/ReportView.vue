<template>
  <AppLayout title="治理报告">
    <section class="page report-grid">
      <div class="panel panel-pad">
        <div class="report-head"><h3 class="section-title">摘要报告</h3><el-button @click="copy">复制</el-button></div>
        <pre>{{ report.summary }}</pre>
        <el-button disabled>导出 PDF</el-button>
        <el-button disabled>导出 DOCX</el-button>
      </div>
      <aside>
        <HotspotCard v-for="item in report.hotspots || []" :key="item.location_name" :item="item" />
      </aside>
    </section>
  </AppLayout>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchReport } from '../api/statistics'
import HotspotCard from '../components/cards/HotspotCard.vue'
import AppLayout from '../components/layout/AppLayout.vue'
const report = ref<any>({ summary: '', hotspots: [] })
async function copy() { await navigator.clipboard.writeText(report.value.summary || '') }
onMounted(async () => { report.value = await fetchReport() })
</script>
<style scoped>
.report-grid { display: grid; grid-template-columns: 1fr 360px; gap: 16px; }
.report-head { display: flex; justify-content: space-between; align-items: center; }
pre { white-space: pre-wrap; line-height: 1.8; color: #334155; font-family: inherit; }
@media (max-width: 980px) { .report-grid { grid-template-columns: 1fr; } }
</style>
