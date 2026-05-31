<template>
  <el-segmented v-model="model" :options="options" />
</template>
<script setup lang="ts">
const model = defineModel<string>({ default: '综合情绪' })
const options = ['综合情绪', '压力', '愉悦', '愤怒', '平静', '数据密度']
</script>
