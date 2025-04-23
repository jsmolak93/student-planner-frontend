// router.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/Home.vue'
import AddStudent from './components/AddStudent.vue'
import StudentPlanner from './components/StudentPlanner.vue'
import CourseSearch from './components/CourseSearch.vue'
import Analytics from './components/Analytics.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/add-student', component: AddStudent },
  { path: '/planner/:studentId', component: StudentPlanner, props: true },
  { path: '/search', component: CourseSearch },
  { path: '/analytics', component: Analytics },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
