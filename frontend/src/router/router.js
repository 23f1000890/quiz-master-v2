import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginPage from '@/views/LoginPage.vue'
import AdminPage from '@/views/AdminPage.vue'
import UserPage from '@/views/UserPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminPage,
      meta: {
        requiresAuth: true,
        role: 'admin',
      }
    },
    {
      path: '/user',
      name: 'user',
      component: UserPage,
      meta: {
        requiresAuth: true,
        role: 'user',
      }
    }
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const role = localStorage.getItem('role')

  if (to.meta.requiresAuth) {
    if (!token || (to.meta.role && role !== to.meta.role)) {
      return next('/login')
    }
  }
  next()
})

export default router
