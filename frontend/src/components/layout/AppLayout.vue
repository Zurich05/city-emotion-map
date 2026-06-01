<template>
  <div class="app-shell">
    <SideMenu />
    <main class="main">
      <TopBar :title="title" />
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import SideMenu from './SideMenu.vue'
import TopBar from './TopBar.vue'
defineProps<{ title: string }>()
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: #f4f7fb;
}

.main {
  margin-left: 252px;
  min-height: 100vh;
  background:
    linear-gradient(180deg, rgba(255,255,255,.72), rgba(244,247,251,0) 180px),
    #f4f7fb;
}

@media (max-width: 900px) {
  .main {
    margin-left: 0;
    padding-top: 64px;
  }
}
</style>
