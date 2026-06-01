<template>
  <AppLayout title="治理建议">
    <section class="page governance">
      <div class="panel panel-pad command">
        <div>
          <span>Governance Suggestion</span>
          <h1>城市情绪治理建议</h1>
          <p>围绕压力、愤怒、忧虑等情绪信号，生成分级处置建议与持续观测清单。</p>
        </div>
        <el-button type="primary" @click="load">重新生成</el-button>
      </div>
      <div class="governance-grid">
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
async function load() { hotspots.value = await fetchHotspots() }
onMounted(load)
</script>

<style scoped>
.governance { display: grid; gap: 22px; }
.command {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: center;
}
.command span { color: #2563eb; font-size: 15px; font-weight: 900; }
.command h1 { margin: 8px 0; color: #102033; font-size: 34px; }
.command p { color: #64748b; line-height: 1.8; margin: 0; font-size: 16px; }
.governance-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(280px, 1fr));
  gap: 22px;
}
@media (max-width: 800px) {
  .command { flex-direction: column; align-items: flex-start; }
  .governance-grid { grid-template-columns: 1fr; }
}
</style>
