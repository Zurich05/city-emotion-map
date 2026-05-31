import { createRouter, createWebHistory } from 'vue-router'
import { currentRole } from '../api/auth'

const routes = [
  { path: '/', component: () => import('../views/LoginView.vue') },
  { path: '/dashboard', component: () => import('../views/DashboardView.vue') },
  { path: '/map', component: () => import('../views/MapView.vue') },
  { path: '/analysis', component: () => import('../views/AnalysisView.vue') },
  { path: '/data', component: () => import('../views/DataManageView.vue') },
  { path: '/users', component: () => import('../views/UserManageView.vue') },
  { path: '/report', component: () => import('../views/ReportView.vue') }
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to) => {
  if (to.path === '/users' && currentRole() !== 'admin') return '/dashboard'
})

export default router
