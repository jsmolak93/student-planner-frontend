<template>
  <div class="charts-page">
    <h1>Analytics Charts</h1>

    <!-- Chart Selection Buttons -->
    <div class="button-group">
      <button @click="selectedChart = 'students'">Students Per Major</button>
      <button @click="selectedChart = 'courses'">Courses Per Department</button>
      <button @click="selectedChart = 'atRisk'">At-Risk Students</button>
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
      <Bar v-if="atRiskChartData" :data="atRiskChartData" :options="chartOptions" />
    </div>
    <div class="back-home-wrapper">
      <RouterLink to="/" class="home-link">← Back to Home</RouterLink>
    </div>
  </div>

</template>

<script>
import { Bar, Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, ArcElement, CategoryScale, LinearScale } from 'chart.js';
import axios from 'axios';

ChartJS.register(Title, Tooltip, Legend, BarElement, ArcElement, CategoryScale, LinearScale);

export default {
  name: 'AnalyticsCharts',
  components: { Bar, Pie },
  data() {
    return {
      selectedChart: '',
      studentsChartData: null,
      coursesChartData: null,
      atRiskChartData: null,
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
        this.loadAtRiskStudents()
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
          labels: Object.keys(counts),
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
          labels: Object.keys(counts),
          datasets: [{
            label: 'Courses',
            data: Object.values(counts),
            backgroundColor: [
              '#ffcc33', '#006633', '#003300', '#009966', '#33cc33',
              '#669900', '#3399ff', '#003366', '#990000', '#cc3300'
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
          labels: Object.keys(counts),
          datasets: [{
            label: 'At-Risk Students',
            data: Object.values(counts),
            backgroundColor: '#cc0000'
          }]
        };
      } catch (err) {
        console.error('Error loading at-risk students', err);
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
  width: 500px;   /* you can adjust this number */
  height: 400px;  /* you can adjust this number */
  margin: 0 auto;
  position: relative; /* Chart.js requires this for sizing */
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
