<template>
  <AppLayout title="数据管理">
    <section class="page grid">
      <ImportPanel @done="load" />
      <div class="panel panel-pad"><h3 class="section-title">样本列表</h3><SampleList :points="points" /></div>
    </section>
  </AppLayout>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchEmotions, type EmotionPoint } from '../api/emotion'
import ImportPanel from '../components/data/ImportPanel.vue'
import SampleList from '../components/data/SampleList.vue'
import AppLayout from '../components/layout/AppLayout.vue'
const points = ref<EmotionPoint[]>([])
async function load() { points.value = await fetchEmotions() }
onMounted(load)
</script>
