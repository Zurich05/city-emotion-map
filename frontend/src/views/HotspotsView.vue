<template>
  <AppLayout title="热点事件">
    <section class="page hotspots-page">
      <div class="page-head panel panel-pad">
        <h1>热点事件监测</h1>
        <p>聚合社交平台中的高频讨论、情绪波动和空间聚集信号，识别需要持续跟踪的城市事件。</p>
      </div>
      <div class="hotspot-grid">
        <HotspotCard v-for="item in hotspots" :key="item.location_name || item.district" :item="item" />
      </div>
    </section>
  </AppLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchHotspots } from '../api/statistics'
import HotspotCard from '../components/cards/HotspotCard.vue'
import AppLayout from '../components/layout/AppLayout.vue'

const hotspots = ref<any[]>([])
onMounted(async () => { hotspots.value = await fetchHotspots() })
</script>

<style scoped>
.hotspots-page { display: grid; gap: 22px; }
.page-head h1 { margin: 0 0 8px; font-size: 34px; color: #102033; }
.page-head p { color: #64748b; line-height: 1.8; margin: 0; font-size: 16px; }
.hotspot-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(260px, 1fr));
  gap: 22px;
}
@media (max-width: 1180px) {
  .hotspot-grid { grid-template-columns: repeat(2, minmax(260px, 1fr)); }
}
@media (max-width: 760px) {
  .hotspot-grid { grid-template-columns: 1fr; }
}
</style>
