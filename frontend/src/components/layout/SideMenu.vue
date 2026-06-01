<template>
  <aside class="side">
    <div class="side-title">
      <span class="side-logo"></span>
      <div>
        <strong>城市情绪地图</strong>
        <small>Government GIS</small>
      </div>
    </div>

    <div class="menu-group">
      <router-link v-for="item in visibleItems" :key="item.path" :to="item.path">
        <span class="icon">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </router-link>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { currentRole } from '../../api/auth'

const items = [
  { path: '/dashboard', label: '分析工作台', icon: '总' },
  { path: '/map', label: '情绪地图', icon: '图' },
  { path: '/analysis', label: '情绪分析', icon: '析' },
  { path: '/data', label: '数据管理', icon: '数' },
  { path: '/hotspots', label: '热点事件', icon: '热' },
  { path: '/governance', label: '治理建议', icon: '治' },
  { path: '/report', label: '报告中心', icon: '报' },
  { path: '/users', label: '用户权限', icon: '权', adminOnly: true }
]

const visibleItems = computed(() => {
  const role = currentRole()
  return items.filter(item => !item.adminOnly || role === 'admin')
})
</script>

<style scoped>
.side {
  width: 252px;
  min-height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 7;
  padding: 22px 16px;
  color: #fff;
  background: linear-gradient(180deg, #102033 0%, #132840 100%);
  border-right: 1px solid rgba(255,255,255,.06);
}

.side-title {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 8px 20px;
  border-bottom: 1px solid rgba(255,255,255,.1);
}

.side-logo {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background:
    radial-gradient(circle at 56% 44%, #60a5fa 0 4px, transparent 5px),
    linear-gradient(#38506b 1px, transparent 1px),
    linear-gradient(90deg, #38506b 1px, transparent 1px),
    #172a42;
  background-size: auto, 10px 10px, 10px 10px, auto;
  border: 1px solid rgba(147,197,253,.32);
}

.side-title strong {
  display: block;
  font-size: 19px;
  line-height: 1.1;
}

.side-title small {
  display: block;
  margin-top: 5px;
  color: #94a3b8;
  font-size: 14px;
}

.menu-group {
  padding-top: 18px;
}

a {
  display: flex;
  align-items: center;
  gap: 13px;
  min-height: 54px;
  color: #cbd5e1;
  text-decoration: none;
  padding: 13px 14px;
  border-radius: 10px;
  margin-bottom: 7px;
  font-size: 17px;
  font-weight: 750;
}

.icon {
  width: 34px;
  height: 34px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #dbeafe;
  background: rgba(255,255,255,.08);
  border-radius: 8px;
  font-size: 15px;
  font-weight: 900;
}

a.router-link-active {
  color: #fff;
  background: #2563eb;
}

a.router-link-active .icon {
  background: rgba(255,255,255,.18);
}

a:hover {
  color: #fff;
  background: rgba(37,99,235,.28);
}

@media (max-width: 900px) {
  .side { display: none; }
}
</style>
