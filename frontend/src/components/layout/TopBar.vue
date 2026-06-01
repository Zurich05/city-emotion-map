<template>
  <header class="topbar">
    <div class="top-title">
      <strong>{{ title }}</strong>
      <small>城市公共情绪空间感知平台</small>
    </div>

    <div class="status">
      <span>在线监测</span>
      <b>武汉市</b>
    </div>

    <button class="avatar" title="退出登录" @click="signOut">U</button>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { logout } from '../../api/auth'

defineProps<{ title: string }>()
const router = useRouter()

function signOut() {
  logout()
  router.push('/')
}
</script>

<style scoped>
.topbar {
  position: sticky;
  top: 0;
  z-index: 5;
  height: 64px;
  padding: 0 28px;
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 18px;
  align-items: center;
  background: rgba(255,255,255,.96);
  border-bottom: 1px solid #e4edf7;
  box-shadow: 0 8px 22px rgba(30, 41, 59, .05);
  backdrop-filter: blur(10px);
}

.top-title strong {
  display: block;
  color: #0f172a;
  font-size: 19px;
  line-height: 1.05;
}

.top-title small {
  display: block;
  margin-top: 4px;
  color: #64748b;
  font-size: 14px;
}

.status {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 7px 10px;
  border-radius: 999px;
  background: #f3f7fc;
  border: 1px solid #e2ebf5;
  color: #64748b;
  font-size: 14px;
}

.status span::before {
  content: "";
  display: inline-block;
  width: 7px;
  height: 7px;
  margin-right: 7px;
  border-radius: 50%;
  background: #10b981;
}

.status b {
  color: #1f3347;
}

.avatar {
  width: 36px;
  height: 36px;
  border: 0;
  border-radius: 50%;
  background: #e9f2ff;
  color: #1d4ed8;
  font-weight: 900;
  cursor: pointer;
}

@media (max-width: 900px) {
  .topbar {
    position: fixed;
    left: 0;
    right: 0;
    padding: 0 18px;
  }

  .status { display: none; }
}
</style>
