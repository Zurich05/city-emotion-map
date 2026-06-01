<template>
  <AppLayout title="数据管理">
    <section class="page grid">
      <ImportPanel @done="load" />
      <div class="panel panel-pad">
        <div class="title-row">
          <h3 class="section-title">数据备份</h3>
          <div class="actions">
            <el-button type="primary" @click="downloadBackup">导出 JSON 备份</el-button>
            <el-upload :show-file-list="false" :auto-upload="false" :on-change="restore">
              <el-button>恢复备份</el-button>
            </el-upload>
          </div>
        </div>
      </div>
      <div class="data-grid">
        <div class="panel panel-pad">
          <div class="title-row">
            <h3 class="section-title">任务日志</h3>
            <el-select v-model="taskType" placeholder="任务类型" clearable style="width:150px" @change="load">
              <el-option label="导入 demo" value="import_demo" />
              <el-option label="采集" value="crawl" />
              <el-option label="清洗" value="clean" />
              <el-option label="情感分析" value="sentiment" />
            </el-select>
          </div>
          <TaskLogTable :logs="logs" />
        </div>
        <div class="panel panel-pad">
          <div class="title-row">
            <h3 class="section-title">操作审计</h3>
            <div class="actions">
              <el-select v-model="auditMethod" placeholder="方法" clearable style="width:110px" @change="load">
                <el-option label="GET" value="GET" />
                <el-option label="POST" value="POST" />
              </el-select>
              <el-input v-model="auditPath" placeholder="路径前缀" clearable style="width:180px" @change="load" />
            </div>
          </div>
          <AuditLogTable :logs="auditLogs" />
        </div>
      </div>
      <div class="panel panel-pad"><h3 class="section-title">样本列表</h3><SampleList :points="points" /></div>
    </section>
  </AppLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { downloadBackup, fetchAuditLogs, restoreBackup } from '../api/admin'
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
const taskType = ref('')
const auditMethod = ref('')
const auditPath = ref('')

async function load() {
  ;[points.value, logs.value, auditLogs.value] = await Promise.all([
    fetchEmotions(),
    fetchImportLogs({ task_type: taskType.value || undefined, limit: 50, offset: 0 }),
    fetchAuditLogs({ method: auditMethod.value || undefined, path: auditPath.value || undefined, limit: 50, offset: 0 })
  ])
}

async function restore(file: any) {
  await restoreBackup(file.raw, true)
  await load()
}

onMounted(load)
</script>

<style scoped>
.data-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(280px, 1fr));
  gap: 16px;
}

@media (max-width: 1000px) {
  .data-grid { grid-template-columns: 1fr; }
}
</style>
