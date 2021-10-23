import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/BlackBox',
    name: 'BlackBox',
    component: () => import('../views/BlackBox.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
