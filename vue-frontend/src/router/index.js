import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import AddStudent from '../components/addStudent.vue'
import StudentPlanner from '../components/StudentPlanner.vue'
import CourseSearch from '../components/CourseSearch.vue'
import CourseRecommendation from '../components/CourseRecommendation.vue'
import Analytics from '../components/Analytics.vue'
import AnalyticsChart from '../components/AnalyticsChart.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/add-student', component: AddStudent },
  { path: '/student-planner', component: StudentPlanner },
  { path: '/course-search', component: CourseSearch },
  { path: '/course-recommendation', component: CourseRecommendation },
  { path: '/analytics', component: Analytics },
  { path: '/visualization', component: AnalyticsChart },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
