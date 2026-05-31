<template>
  <AppLayout title="数据管理">
    <section class="page grid">
      <ImportPanel @done="load" />
      <div class="panel panel-pad">
        <div class="title-row">
          <h3 class="section-title">备份</h3>
          <el-button type="primary" @click="downloadBackup">导出 JSON 备份</el-button>
        </div>
      </div>
      <div class="panel panel-pad"><h3 class="section-title">任务日志</h3><TaskLogTable :logs="logs" /></div>
      <div class="panel panel-pad"><h3 class="section-title">操作审计</h3><AuditLogTable :logs="auditLogs" /></div>
      <div class="panel panel-pad"><h3 class="section-title">样本列表</h3><SampleList :points="points" /></div>
    </section>
  </AppLayout>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { downloadBackup, fetchAuditLogs } from '../api/admin'
import { fetchEmotions, type EmotionPoint } from '../api/emotion'
import { fetchImportLogs } from '../api/importData'
import AuditLogTable from '../components/data/AuditLogTable.vue'
import ImportPanel from '../components/data/ImportPanel.vue'
import SampleList from '../components/data/SampleList.vue'
import TaskLogTable from '../components/data/TaskLogTable.vue'
import AppLayout from '../components/layout/AppLayout.vue'
const points = ref<EmotionPoint[]>([])
const logs = ref<any[]>([])
const auditLogs = ref<any[]>([])
async function load() {
  ;[points.value, logs.value, auditLogs.value] = await Promise.all([fetchEmotions(), fetchImportLogs(), fetchAuditLogs()])
}
onMounted(load)
</script>

<style scoped>
.title-row { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.title-row .section-title { margin: 0; }
</style>
