<template>
  <section class="login">
    <div class="map-background" aria-hidden="true">
      <span v-for="road in roads" :key="road" :class="['road', road]"></span>
      <span v-for="spot in spots" :key="spot.class" :class="['heat-dot', spot.class]"></span>
      <span class="river"></span>
    </div>

    <div class="hero-copy">
      <span class="eyebrow">City Emotion Map</span>
      <h1>
        城市情绪地图
        <small>City Emotion Map</small>
      </h1>
      <p>基于社交媒体文本情感分析的城市公共情绪空间感知平台</p>
      <div class="capabilities">
        <b>情绪识别</b>
        <b>热点发现</b>
        <b>空间分析</b>
        <b>治理建议</b>
      </div>
    </div>

    <div class="form-panel">
      <div class="form-head">
        <h2>平台登录</h2>
        <p>进入城市情绪分析与空间治理工作台</p>
      </div>
      <el-input v-model="username" placeholder="账号" size="large" />
      <el-input v-model="password" placeholder="密码" type="password" size="large" show-password />
      <el-alert v-if="error" :title="error" type="error" :closable="false" />
      <el-button type="primary" size="large" :loading="loading" @click="submit">登录系统</el-button>
      <div class="form-foot">
        <span>默认账号：admin</span>
        <span>政务 GIS 专业版</span>
      </div>
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
const roads = ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8']
const spots = [
  { class: 'positive' },
  { class: 'calm' },
  { class: 'stress' },
  { class: 'anger' },
  { class: 'worry' },
  { class: 'positive alt' },
  { class: 'calm alt' },
  { class: 'stress alt' }
]

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
.login {
  min-height: 100vh;
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(500px, 540px);
  gap: clamp(36px, 5vw, 84px);
  align-items: center;
  padding: clamp(34px, 5vw, 60px) clamp(46px, 6vw, 78px) clamp(42px, 6vw, 76px);
  overflow: hidden;
  background:
    linear-gradient(120deg, rgba(247,250,254,.94) 0%, rgba(240,246,253,.9) 54%, rgba(231,240,250,.86) 100%),
    #eef4fb;
}

.map-background {
  position: absolute;
  inset: 0;
  opacity: .42;
  background:
    linear-gradient(#cfddeb 1px, transparent 1px),
    linear-gradient(90deg, #cfddeb 1px, transparent 1px),
    radial-gradient(circle at 34% 48%, rgba(37,99,235,.08), transparent 28%),
    #eef5fc;
  background-size: 52px 52px, 52px 52px, auto, auto;
}

.road {
  position: absolute;
  height: 2px;
  border-radius: 999px;
  background: #8fa7c0;
  opacity: .7;
}

.r1 { left: -8%; top: 22%; width: 66%; transform: rotate(8deg); }
.r2 { left: 14%; top: 36%; width: 78%; transform: rotate(-13deg); }
.r3 { left: 2%; top: 62%; width: 70%; transform: rotate(15deg); }
.r4 { left: 42%; top: 10%; width: 2px; height: 74%; transform: rotate(28deg); }
.r5 { left: 62%; top: 0; width: 2px; height: 86%; transform: rotate(-18deg); }
.r6 { left: 26%; top: 6%; width: 2px; height: 78%; transform: rotate(6deg); }
.r7 { left: 46%; top: 78%; width: 62%; transform: rotate(-7deg); }
.r8 { left: 8%; top: 84%; width: 52%; transform: rotate(4deg); }

.river {
  position: absolute;
  left: -12%;
  top: 48%;
  width: 128%;
  height: 90px;
  border-radius: 50%;
  border-top: 22px solid rgba(77, 137, 190, .22);
  transform: rotate(-8deg);
}

.heat-dot {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,.95);
  box-shadow: 0 0 0 5px rgba(255,255,255,.34), 0 8px 18px rgba(30,41,59,.18);
}

.positive { left: 18%; top: 32%; background: #10b981; }
.calm { left: 48%; top: 24%; background: #3b82f6; }
.stress { left: 62%; top: 55%; background: #f59e0b; }
.anger { left: 36%; top: 66%; background: #ef4444; }
.worry { left: 76%; top: 38%; background: #8b5cf6; }
.positive.alt { left: 58%; top: 74%; }
.calm.alt { left: 24%; top: 78%; }
.stress.alt { left: 84%; top: 66%; }

.hero-copy,
.form-panel {
  position: relative;
  z-index: 1;
}

.hero-copy {
  max-width: 900px;
  align-self: start;
  margin-top: clamp(58px, 10vh, 112px);
  margin-left: clamp(18px, 3vw, 54px);
}

.eyebrow {
  display: inline-block;
  color: #2563eb;
  font-size: 20px;
  font-weight: 900;
  letter-spacing: .02em;
  margin-bottom: 18px;
}

h1 {
  margin: 0;
  color: #132033;
  font-size: clamp(96px, 9.4vw, 138px);
  line-height: .98;
  letter-spacing: 0;
}

h1 small {
  display: block;
  margin-top: 14px;
  color: #2f4055;
  font-size: clamp(50px, 5.2vw, 76px);
  font-weight: 750;
}

.hero-copy p {
  max-width: 780px;
  margin: 28px 0 0;
  color: #40556b;
  font-size: 24px;
  line-height: 1.7;
  font-weight: 600;
}

.capabilities {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 38px;
}

.capabilities b {
  padding: 13px 19px;
  border-radius: 999px;
  color: #1d4ed8;
  background: rgba(255,255,255,.9);
  border: 1px solid #d7e5f4;
  font-size: 18px;
  box-shadow: 0 8px 18px rgba(30,41,59,.06);
}

.form-panel {
  width: 100%;
  min-height: 560px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 24px;
  padding: 54px;
  background: #fff;
  border: 1px solid #edf2f8;
  border-radius: 20px;
  box-shadow: 0 26px 70px rgba(30, 41, 59, .14);
}

.form-head h2 {
  margin: 0;
  color: #0f172a;
  font-size: 36px;
}

.form-head p {
  margin: 8px 0 8px;
  color: #334155;
  font-size: 18px;
}

.form-panel :deep(.el-input__wrapper) {
  min-height: 62px;
  padding: 1px 18px;
}

.form-panel :deep(.el-input__inner) {
  font-size: 18px !important;
}

.form-panel :deep(.el-button) {
  height: 62px;
  margin-top: 6px;
  font-size: 18px;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  border: 0;
}

.form-foot {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  color: #64748b;
  font-size: 15px;
  font-weight: 650;
}

@media (max-width: 980px) {
  .login {
    grid-template-columns: 1fr;
    padding: 34px 22px;
  }

  .form-panel {
    max-width: 480px;
  }
}

@media (max-width: 640px) {
  h1 { font-size: 52px; }
  h1 small { font-size: 30px; }
  .hero-copy p { font-size: 18px; }
  .form-panel { padding: 34px; }
}
</style>
