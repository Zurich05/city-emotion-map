<template>
  <aside class="side">
    <div class="brand">城市情绪地图</div>
    <router-link v-for="item in visibleItems" :key="item.path" :to="item.path">{{ item.label }}</router-link>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { currentRole } from '../../api/auth'

const items = [
  { path: '/dashboard', label: '仪表盘' },
  { path: '/map', label: '情绪地图' },
  { path: '/analysis', label: '分析' },
  { path: '/data', label: '数据管理' },
  { path: '/users', label: '用户权限', adminOnly: true },
  { path: '/report', label: '报告' }
]

const visibleItems = computed(() => {
  const role = currentRole()
  return items.filter(item => !item.adminOnly || role === 'admin')
})
</script>

<style scoped>
.side { width: 216px; min-height: 100vh; background: #101828; color: #fff; padding: 22px 14px; position: fixed; left: 0; top: 0; }
.brand { font-weight: 800; font-size: 19px; margin: 0 8px 24px; }
a { display: block; color: #cbd5e1; text-decoration: none; padding: 12px 14px; border-radius: 8px; margin-bottom: 6px; }
a.router-link-active, a:hover { color: #fff; background: #2563eb; }
</style>
