import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import AuthView from '../views/AuthView.vue'
import App from '../App.vue'

const routes = [
  {
    path: '/auth',
    name: 'Auth',
    component: AuthView,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Home',
    component: App,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth) {
    const isAuthenticated = await authStore.checkAuth()
    if (!isAuthenticated) {
      next('/auth')
    } else {
      next()
    }
  } else if (to.path === '/auth' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
