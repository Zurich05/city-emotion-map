import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('../views/LoginView.vue') },
  { path: '/dashboard', component: () => import('../views/DashboardView.vue') },
  { path: '/map', component: () => import('../views/MapView.vue') },
  { path: '/analysis', component: () => import('../views/AnalysisView.vue') },
  { path: '/data', component: () => import('../views/DataManageView.vue') },
  { path: '/report', component: () => import('../views/ReportView.vue') }
]

export default createRouter({ history: createWebHistory(), routes })
