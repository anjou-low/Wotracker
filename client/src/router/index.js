import { createRouter, createWebHistory } from 'vue-router'
import { store } from '../store/store'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import WorkoutView from '../views/WorkoutView.vue'
import ExerciseView from '../views/ExerciseView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/workouts/:workoutId',
      name: 'workout',
      component: WorkoutView
    },
    {
      path: '/workouts/:workoutId/exercises/:exerciseId',
      name: 'exercise',
      component: ExerciseView
    }
  ]
})

router.beforeEach(async (to, from) => {
  if (store.isLoggedIn === false && to.name !== 'login') {
    return { name: 'login' }
  }
})

export default router
