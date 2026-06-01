<template>
  <div class="keyword-cloud">
    <span v-for="item in words" :key="item.text" :style="{ fontSize: item.size + 'px', color: item.color }">
      {{ item.text }}
    </span>
  </div>
</template>

<script setup lang="ts">
const words = [
  { text: '通勤压力', size: 26, color: '#d99a4e' },
  { text: '夜间安全', size: 19, color: '#9a78c7' },
  { text: '地铁拥挤', size: 23, color: '#d95f68' },
  { text: '公园舒适', size: 21, color: '#4fb783' },
  { text: '消费活力', size: 17, color: '#4d8fd8' },
  { text: '噪声扰民', size: 20, color: '#d99a4e' },
  { text: '办事效率', size: 16, color: '#4fb783' },
  { text: '道路施工', size: 18, color: '#d95f68' },
  { text: '社区服务', size: 22, color: '#4d8fd8' },
  { text: '旅游热度', size: 19, color: '#9a78c7' }
]
</script>

<style scoped>
.keyword-cloud {
  min-height: 250px;
  display: flex;
  align-items: center;
  align-content: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 14px 18px;
  padding: 16px;
}

span {
  font-weight: 900;
  white-space: nowrap;
  opacity: .92;
}
</style>
