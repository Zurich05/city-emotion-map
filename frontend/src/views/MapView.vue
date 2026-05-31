<template>
  <AppLayout title="情绪地图">
    <section class="page">
      <div class="toolbar">
        <LayerControl v-model="layer" />
        <el-button type="primary" @click="load">刷新</el-button>
      </div>
      <div class="map-grid">
        <div class="panel"><EmotionMap :points="points" :layer="layer" /></div>
        <aside>
          <HotspotCard v-for="item in hotspots" :key="item.location_name" :item="item" />
        </aside>
      </div>
    </section>
  </AppLayout>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchEmotions, type EmotionPoint } from '../api/emotion'
import { fetchHotspots } from '../api/statistics'
import HotspotCard from '../components/cards/HotspotCard.vue'
import AppLayout from '../components/layout/AppLayout.vue'
import EmotionMap from '../components/map/EmotionMap.vue'
import LayerControl from '../components/map/LayerControl.vue'
const points = ref<EmotionPoint[]>([])
const hotspots = ref<any[]>([])
const layer = ref('综合情绪')
async function load() { points.value = await fetchEmotions(); hotspots.value = await fetchHotspots() }
onMounted(load)
</script>
<style scoped>
.map-grid { display: grid; grid-template-columns: 1fr 360px; gap: 16px; align-items: start; }
aside { max-height: calc(100vh - 178px); overflow: auto; }
@media (max-width: 1100px) { .map-grid { grid-template-columns: 1fr; } }
</style>
