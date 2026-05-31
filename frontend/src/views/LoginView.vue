<template>
  <section class="login">
    <div class="login-box panel">
      <h1>城市情绪地图系统</h1>
      <p>面向公开文本数据的城市情绪分析与治理辅助平台</p>
      <el-input v-model="username" placeholder="账号" />
      <el-input v-model="password" placeholder="密码" type="password" />
      <el-alert v-if="error" :title="error" type="error" :closable="false" />
      <el-button type="primary" size="large" :loading="loading" @click="submit">进入系统</el-button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api/auth'

const router = useRouter()
const username = ref('admin')
const password = ref('admin123')
const loading = ref(false)
const error = ref('')

async function submit() {
  loading.value = true
  error.value = ''
  try {
    await login(username.value, password.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = err instanceof Error ? err.message : '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login { min-height: 100vh; display: grid; place-items: center; background: radial-gradient(circle at 20% 20%, rgba(37,99,235,.28), transparent 32%), linear-gradient(135deg, #eef6ff, #fff7ed 55%, #f5f3ff); }
.login-box { width: min(420px, calc(100vw - 36px)); padding: 34px; display: grid; gap: 16px; }
h1 { margin: 0; font-size: 30px; }
p { margin: 0 0 12px; color: #64748b; }
</style>
