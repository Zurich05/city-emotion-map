<template>
  <div class="panel panel-pad">
    <h3 class="section-title">数据任务</h3>
    <div class="toolbar">
      <el-input v-model="keyword" placeholder="关键词" style="width:160px" />
      <el-select v-model="platform" style="width:130px">
        <el-option label="模拟" value="mock" />
        <el-option label="微博" value="weibo" />
        <el-option label="小红书" value="xhs" />
        <el-option label="抖音" value="douyin" />
      </el-select>
      <el-button type="primary" @click="crawl">模拟采集</el-button>
      <el-button type="success" @click="demo">导入 demo</el-button>
      <el-button @click="clean">清洗</el-button>
      <el-button @click="sentiment">情感分析</el-button>
      <el-upload :show-file-list="false" :auto-upload="false" :on-change="upload">
        <el-button>上传文件</el-button>
      </el-upload>
    </div>
    <el-alert v-if="message" :title="message" type="success" :closable="false" />
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { runClean, runSentiment, startCrawl } from '../../api/crawl'
import { importDemoData, uploadData } from '../../api/importData'
const emit = defineEmits<{ done: [] }>()
const keyword = ref('地铁')
const platform = ref('mock')
const message = ref('')
async function crawl() { message.value = JSON.stringify(await startCrawl({ platform: platform.value, keyword: keyword.value, limit: 80 })); emit('done') }
async function demo() { message.value = JSON.stringify(await importDemoData()); emit('done') }
async function clean() { message.value = JSON.stringify(await runClean()); emit('done') }
async function sentiment() { message.value = JSON.stringify(await runSentiment()); emit('done') }
async function upload(file: any) { message.value = JSON.stringify(await uploadData(file.raw, platform.value)); emit('done') }
</script>
