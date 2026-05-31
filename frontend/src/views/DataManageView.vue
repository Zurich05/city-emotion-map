<template>
  <AppLayout title="数据管理">
    <section class="page grid">
      <ImportPanel @done="load" />
      <div class="panel panel-pad"><h3 class="section-title">任务日志</h3><TaskLogTable :logs="logs" /></div>
      <div class="panel panel-pad"><h3 class="section-title">样本列表</h3><SampleList :points="points" /></div>
    </section>
  </AppLayout>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchEmotions, type EmotionPoint } from '../api/emotion'
import { fetchImportLogs } from '../api/importData'
import ImportPanel from '../components/data/ImportPanel.vue'
import SampleList from '../components/data/SampleList.vue'
import TaskLogTable from '../components/data/TaskLogTable.vue'
import AppLayout from '../components/layout/AppLayout.vue'
const points = ref<EmotionPoint[]>([])
const logs = ref<any[]>([])
async function load() {
  ;[points.value, logs.value] = await Promise.all([fetchEmotions(), fetchImportLogs()])
}
onMounted(load)
</script>
