import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginPage from '@/views/LoginPage.vue'
import AdminPage from '@/views/AdminPage.vue'
import UserPage from '@/views/UserPage.vue'
import AddSubject from '@/views/AddSubject.vue'
import UserDetails from '@/views/UserDetails.vue'
import EditSubject from '@/views/EditSubject.vue'
import QuizDash from '@/views/QuizDash.vue'
import AddChapter from '@/views/AddChapter.vue'
import EditChapter from '@/views/EditChapter.vue'
import AddQuiz from '@/views/AddQuiz.vue'
import EditQuiz from '@/views/EditQuiz.vue'
import AddQuestion from '@/views/AddQuestion.vue'
import EditQuestion from '@/views/EditQuestion.vue'

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
    },
    {
      path: '/add_subject',
      name: 'add_subject',
      component: AddSubject,
    },
    {
      path: '/edit_subject/:subject_id',
      name: 'edit_subject',
      component: EditSubject,
    },
    {
      path: '/add_chapter/:subject_id',
      name: 'add_chapter',
      component: AddChapter,
    },
    {
      path: '/edit_chapter/:chapter_id',
      name: 'edit_chapter',
      component: EditChapter,
    },
    {
      path: '/admin/quiz_dash',
      name: 'quiz_dash',
      component: QuizDash,
    },
    {
      path: '/admin/add_quiz',
      name: 'add_quiz',
      component: AddQuiz,
    },
    {
      path: '/admin/edit_quiz/:quiz_id',
      name: 'edit_quiz',
      component: EditQuiz,
    },
    {
      path: '/admin/add_question/:quiz_id',
      name: 'add_question',
      component: AddQuestion,
    },
    {
      path: '/admin/edit_question/:question_id',
      name: 'edit_question',
      component: EditQuestion,
    },
    {
      path: '/user_details',
      name: 'UserDetails',
      component: UserDetails,
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
