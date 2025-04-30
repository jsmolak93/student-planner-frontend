<template>
  <div class="charts-page">
    <h1>Analytics Charts</h1>

    <!-- Chart Selection Buttons -->
    <div class="button-group">
      <button @click="selectedChart = 'students'">Students Per Major</button>
      <button @click="selectedChart = 'courses'">Courses Per Department</button>
      <button @click="selectedChart = 'atRisk'">At-Risk Students</button>
      <button @click="selectedChart = 'instructorWorkload'">Instructor Workload</button>
      <button @click="selectedChart = 'studentUnits'">Student Units</button>
    </div>

    <!-- Chart Rendering -->
 
    <div class="chart-wrapper" v-if="selectedChart === 'students'">
      <h2>Number of Students Per Major</h2>
      <Bar v-if="studentsChartData" :data="studentsChartData" :options="chartOptions" />
    </div>

    <div class="chart-wrapper" v-if="selectedChart === 'courses'">
      <h2>Course Distribution by Department</h2>
      <Pie v-if="coursesChartData" :data="coursesChartData" :options="chartOptions" />
    </div>

    <div class="chart-wrapper" v-if="selectedChart === 'atRisk'">
      <h2>At-Risk Students Per Major</h2>
      <Doughnut v-if="atRiskChartData" :data="atRiskChartData" :options="chartOptions" />
    </div>

    <div class="chart-wrapper" v-if="selectedChart === 'instructorWorkload'">
      <h2>Instructor Workload</h2>
      <Pie v-if="instructorWorkloadData" :data="instructorWorkloadData" :options="chartOptions" />
    </div>

    <div class="chart-wrapper" v-if="selectedChart === 'studentUnits'">
      <h2>Student Units Completed</h2>
      <Bar v-if="studentUnitsData" :data="studentUnitsData" :options="chartOptions" />
    </div>
    <div class="back-home-wrapper">
      <RouterLink to="/" class="home-link">← Back to Home</RouterLink>
    </div>
  </div>

</template>

<script>
import { Bar, Doughnut, Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, ArcElement, CategoryScale, LinearScale } from 'chart.js';
import axios from 'axios';

ChartJS.register(Title, Tooltip, Legend, BarElement, ArcElement, CategoryScale, LinearScale);

export default {
  name: 'AnalyticsCharts',
  components: { Bar, Pie, Doughnut},
  data() {
    return {
      selectedChart: '',
      studentsChartData: null,
      coursesChartData: null,
      atRiskChartData: null,
      instructorWorkloadData: null,
      studentUnitsData: null,

      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',  
            labels: {
              boxWidth: 20,
              padding: 15,
            }
          }
        },
      }
    };
  },

  async mounted() {
    try {
      await Promise.all([
        this.loadStudentsPerMajor(),
        this.loadCoursesPerDepartment(),
        this.loadAtRiskStudents(),  
        this.loadInstructorWorkload(),
        this.loadStudentUnits()
      ]);
    } catch (err) {
      console.error('Error mounting charts', err);
    }
  },

  methods: {
    async loadStudentsPerMajor() {
      try {
        const res = await axios.get('/api/charts/students-by-major');
        const counts = res.data;

        this.studentsChartData = {
          labels: Object.keys(counts).map(label =>
            label
              .split('_')
              .map(word => word.charAt(0).toUpperCase() + word.slice(1))
              .join(' ')
            ),

            datasets: [{
            label: 'Students',
            data: Object.values(counts),
            backgroundColor: '#006633'
          }]
        };
      } catch (err) {
        console.error('Error loading students per major', err);
      }
    },

    async loadCoursesPerDepartment() {
      try {
        const res = await axios.get('/api/charts/courses-by-department');
        const counts = res.data;

        this.coursesChartData = {
          labels: Object.keys(counts).map(label =>
            label
              .split('_')
              .map(word => word.charAt(0).toUpperCase() + word.slice(1))
              .join(' ')
            ),
            datasets: [{
            label: 'Courses',
            data: Object.values(counts),
            backgroundColor: [
              '#E6194B', // Red
              '#3CB44B', // Green
              '#4363D8', // Blue
              '#F58231', // Orange
              '#911EB4', // Purple
              '#46F0F0', // Cyan
              '#FFD700', // Gold
              '#000000', // Black
              '#9A6324', // Brown
              '#42D4F4', // Sky Blue
            ]
          }]
        };
      } catch (err) {
        console.error('Error loading courses per department', err);
      }
    },

    async loadAtRiskStudents() {
      try {
        const res = await axios.get('/api/charts/at-risk-by-major');
        const counts = res.data;

        this.atRiskChartData = {
          labels: Object.keys(counts).map(label =>
            label
              .split('_')
              .map(word => word.charAt(0).toUpperCase() + word.slice(1))
              .join(' ')
          ),
          datasets: [{
            label: 'At-Risk Students',
            data: Object.values(counts),
            backgroundColor: [
              '#E6194B', // Red
              '#3CB44B', // Green
              '#4363D8', // Blue
              '#FFD700', // Yellow
              '#F58231', // Orange
              '#000000', // Black
              '#9A6324', // Brown
              '#42D4F4', // Cyan
            ]
          }]
        };
      } catch (err) {
        console.error('Error loading at-risk students', err);
      }
    },
    async loadInstructorWorkload() {
      try {
        const res = await axios.get("/api/charts/instructor-workload");
        const counts = res.data;
        this.instructorWorkloadData = {
          labels: Object.keys(counts),
          datasets: [{
            label: "Courses Taught",
            data: Object.values(counts),
            backgroundColor: [
              '#E6194B', // Vivid Red
              '#3CB44B', // Vivid Green
              '#FFE119', // Bright Yellow
              '#0082C8', // Strong Blue
              '#F58231', // Orange
              '#46F0F0', // Cyan
              '#F032E6', // Magenta
              '#D2F53C', // Lime
              '#008080', // Teal
              '#AA6E28', // Brown
              '#800000', // Maroon
              '#000075', // Navy Blue
              '#808000', // Olive
              '#808080', // Gray
              '#000000'  // Black
            ]
          }]
        };
      } catch (err) {
        console.error("Failed to load instructor workload", err);
      }
    },

    async loadStudentUnits() {
      try {
        const res = await axios.get("/api/charts/student-units");
        const counts = res.data;
        this.studentUnitsData = {
          labels: Object.keys(counts),
          datasets: [{
            label: "Units Completed",
            data: Object.values(counts),
            backgroundColor: "#ffcc33"
          }]
        };
      } catch (err) {
        console.error("Failed to load student units", err);
      }
    }
  }
};
</script>



<style scoped>
.back-home-wrapper {
  padding-top: 50px;
  margin-top: 30px;
  text-align: center;
}

.button-group {
  margin-bottom: 30px;
}

.button-group button {
  margin: 0 10px;
  padding: 10px 20px;
  font-size: 1rem;
  background-color: #006633;
  color: #ffcc33;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.button-group button:hover {
  background-color: #004d26;
  color: #ffffff;
}
.chart-wrapper {
  width: 500px;   
  height: 400px;  
  margin: 0 auto;
  position: relative;
}

.charts-page {
  padding: 30px;
  background-color: #ffffff;
  text-align: center;
}

.chart-section {
  margin-bottom: 40px;
}

.home-link {
  display: block;
  margin-top: 30px;
  color: #006633;
  font-weight: bold;
  text-decoration: none;
}
.home-link:hover {
  text-decoration: underline;
}
</style>
