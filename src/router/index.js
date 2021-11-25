import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/BlackBox',
    name: 'BlackBox',
    component: () => import('../views/BlackBox.vue')
  },
  {
    path: '/Lottery',
    name: 'Lottery',
    component: () => import('../views/Lottery.vue')
  },
  {
    path: '/Bingo-discounts',
    name: 'Bingo-discounts',
    component: () => import('../views/Bingo-discounts.vue')
  },
  {
    path: '/Bingo-boosters',
    name: 'Bingo-boosters',
    component: () => import('../views/Bingo-boosters.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
