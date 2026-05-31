<template>
  <AppLayout title="用户与权限">
    <section class="page user-grid">
      <div class="panel panel-pad">
        <h3 class="section-title">新增用户</h3>
        <el-form label-position="top">
          <el-form-item label="用户名"><el-input v-model="form.username" /></el-form-item>
          <el-form-item label="密码"><el-input v-model="form.password" type="password" /></el-form-item>
          <el-form-item label="角色">
            <el-select v-model="form.role" style="width:100%">
              <el-option label="管理员" value="admin" />
              <el-option label="分析员" value="analyst" />
              <el-option label="查看者" value="viewer" />
            </el-select>
          </el-form-item>
          <el-button type="primary" @click="submit">创建</el-button>
        </el-form>
      </div>
      <div class="panel panel-pad">
        <h3 class="section-title">用户列表</h3>
        <el-table :data="users" height="520">
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="role" label="角色" width="130">
            <template #default="{ row }">
              <el-select v-model="row.role" size="small" @change="save(row)">
                <el-option label="管理员" value="admin" />
                <el-option label="分析员" value="analyst" />
                <el-option label="查看者" value="viewer" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column prop="is_active" label="启用" width="100">
            <template #default="{ row }">
              <el-switch v-model="row.is_active" @change="save(row)" />
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="190" />
        </el-table>
      </div>
    </section>
  </AppLayout>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { createUser, fetchUsers, updateUser, type UserRecord } from '../api/users'
import AppLayout from '../components/layout/AppLayout.vue'

const users = ref<UserRecord[]>([])
const form = reactive({ username: '', password: '', role: 'viewer' })

async function load() { users.value = await fetchUsers() }
async function submit() {
  await createUser(form)
  form.username = ''
  form.password = ''
  form.role = 'viewer'
  await load()
}
async function save(row: UserRecord) {
  await updateUser(row.id, { role: row.role, is_active: row.is_active })
}
onMounted(load)
</script>

<style scoped>
.user-grid { display: grid; grid-template-columns: 340px 1fr; gap: 16px; }
@media (max-width: 900px) { .user-grid { grid-template-columns: 1fr; } }
</style>
