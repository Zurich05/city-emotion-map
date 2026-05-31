<template>
  <SideMenu />
  <main class="main">
    <TopBar :title="title" />
    <slot />
  </main>
</template>

<script setup lang="ts">
import SideMenu from './SideMenu.vue'
import TopBar from './TopBar.vue'
defineProps<{ title: string }>()
</script>

<style scoped>
.main { margin-left: 216px; min-height: 100vh; }
@media (max-width: 760px) { .main { margin-left: 0; } }
</style>
