<template>
  <section class="login">
    <div class="login-box panel">
      <h1>城市情绪地图系统</h1>
      <p>面向公开文本数据的城市情绪分析与治理辅助平台</p>
      <el-input placeholder="演示账号" model-value="guest" />
      <el-input placeholder="演示密码" model-value="demo" type="password" />
      <el-button type="primary" size="large" @click="$router.push('/dashboard')">游客演示进入</el-button>
    </div>
  </section>
</template>

<style scoped>
.login { min-height: 100vh; display: grid; place-items: center; background: radial-gradient(circle at 20% 20%, rgba(37,99,235,.28), transparent 32%), linear-gradient(135deg, #eef6ff, #fff7ed 55%, #f5f3ff); }
.login-box { width: min(420px, calc(100vw - 36px)); padding: 34px; display: grid; gap: 16px; }
h1 { margin: 0; font-size: 30px; }
p { margin: 0 0 12px; color: #64748b; }
</style>
