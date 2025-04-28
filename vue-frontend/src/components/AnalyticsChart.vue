<template>
    <div class="charts-page">
      <h1>Analytics Charts</h1>
  
      <div class="chart-section">
        <h2>Number of Students per Major</h2>
        <Bar v-if="studentsChartData" :data="studentsChartData" :options="chartOptions" />
      </div>
  
      <div class="chart-section">
        <h2>Course Distribution by Department</h2>
        <Pie v-if="coursesChartData" :data="coursesChartData" :options="chartOptions" />
      </div>
  
      <div class="chart-section">
        <h2>At-Risk Students per Major</h2>
        <Bar v-if="atRiskChartData" :data="atRiskChartData" :options="chartOptions" />
      </div>
  
      <RouterLink to="/" class="home-link">← Back to Home</RouterLink>
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
        studentsChartData: null,
        coursesChartData: null,
        atRiskChartData: null,
        chartOptions: {
          responsive: true,
          plugins: {
            legend: { position: 'top' },
          },
        }
      };
    },
    async mounted() {
      await Promise.all([
        this.loadStudentsPerMajor(),
        this.loadCoursesPerDepartment(),
        this.loadAtRiskStudents()
      ]);
    },
    methods: {
      async loadStudentsPerMajor() {
        try {
          const res = await axios.get('/api/students');
          const counts = {};
          res.data.forEach(student => {
            counts[student.major] = (counts[student.major] || 0) + 1;
          });
  
          this.studentsChartData = {
            labels: Object.keys(counts),
            datasets: [{
              label: 'Students',
              data: Object.values(counts),
              backgroundColor: '#006633'  // GMU green
            }]
          };
        } catch (err) {
          console.error('Error loading students per major', err);
        }
      },
      async loadCoursesPerDepartment() {
        try {
          const res = await axios.get('/api/courses');
          const counts = {};
          res.data.forEach(course => {
            counts[course.dcode] = (counts[course.dcode] || 0) + 1;
          });
  
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
          const res = await axios.get('/api/at-risk-students');
          const counts = {};
          res.data.forEach(student => {
            counts[student.major] = (counts[student.major] || 0) + 1;
          });
  
          this.atRiskChartData = {
            labels: Object.keys(counts),
            datasets: [{
              label: 'At-Risk Students',
              data: Object.values(counts),
              backgroundColor: '#cc0000' // Red for danger
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
  .charts-page {
    padding: 40px;
    text-align: center;
    background: white;
  }
  .chart-section {
    margin-bottom: 50px;
  }
  .home-link {
    display: block;
    margin-top: 30px;
    font-weight: bold;
    color: #006633;
    text-decoration: none;
  }
  </style>
  