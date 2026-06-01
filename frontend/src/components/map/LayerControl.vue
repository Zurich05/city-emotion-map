<template>
  <div class="layer-control">
    <div class="switch-row">
      <div>
        <strong>情绪热力图</strong>
        <span>低强度叠加</span>
      </div>
      <el-switch v-model="heatModel" />
    </div>

    <button
      v-for="option in options"
      :key="option"
      :class="{ active: model === option }"
      @click="model = option"
    >
      <i :style="{ background: colorFor(option) }"></i>
      {{ option }}
    </button>
  </div>
</template>

<script setup lang="ts">
const model = defineModel<string>({ default: '综合情绪' })
const heatModel = defineModel<boolean>('heat', { default: false })
const options = ['综合情绪', '数据密度', '积极', '平静', '压力', '愤怒', '忧虑']

function colorFor(option: string) {
  return ({
    综合情绪: '#2563eb',
    数据密度: '#64748b',
    积极: '#10b981',
    平静: '#3b82f6',
    压力: '#f59e0b',
    愤怒: '#ef4444',
    忧虑: '#8b5cf6'
  } as Record<string, string>)[option] || '#2563eb'
}
</script>

<style scoped>
.layer-control {
  display: grid;
  gap: 9px;
}

.switch-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 6px;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #dbe6f2;
  background: #f8fbff;
}

.switch-row strong,
.switch-row span {
  display: block;
}

.switch-row strong {
  color: #172033;
  font-size: 15px;
}

.switch-row span {
  margin-top: 3px;
  color: #64748b;
  font-size: 13px;
}

button {
  width: 100%;
  min-height: 48px;
  display: flex;
  align-items: center;
  gap: 9px;
  text-align: left;
  border: 1px solid #dbe5ef;
  background: #fff;
  color: #334155;
  border-radius: 10px;
  padding: 12px 13px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 750;
}

button i {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(226,235,245,.9);
}

button:hover,
button.active {
  color: #1d4ed8;
  border-color: #bfdbfe;
  background: #eff6ff;
}
</style>
