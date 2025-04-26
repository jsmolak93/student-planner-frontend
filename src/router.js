// router.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/Home.vue'
import AddStudent from './components/AddStudent.vue'
import StudentPlanner from './components/StudentPlanner.vue'
import CourseSearch from './components/CourseSearch.vue'
import Analytics from './components/Analytics.vue'
import CourseRecommendation from '../components/CourseRecommendation.vue';



const routes = [
  { path: '/', component: Home },
  { path: '/add-student', component: AddStudent },
  { path: '/planner/:studentId', component: StudentPlanner, props: true },
  { path: '/search', component: CourseSearch },
  { path: '/analytics', component: Analytics },
  { path: '/recommendations', component: CourseRecommendation},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
