<template>
  <div class="page-container">
    <img src="/mason_logo.png" alt="Background" class="background-overlay" />
    <img src="/mason_mascot.png" alt="GMU Logo" class="logo-top-left" />

    <div class="form-wrapper">
      <h1 class="page-title">Course Recommendations</h1>

      <div class="input-group">
        <input
          v-model="ssn"
          type="number"
          placeholder="Enter Student SSN..."
          class="input-field"
        />
        <button @click="fetchRecommendations" class="primary-button">
          Get Recommendations
        </button>
      </div>

      <div v-if="recommendedCourses.length > 0" class="results">
        <h2>Recommended Courses</h2>
        <ul>
          <li v-for="course in recommendedCourses" :key="`${course.dcode}-${course.cno}`">
            <strong>{{ course.dcode }} {{ course.cno }}</strong> - {{ course.title }}
          </li>
        </ul>
      </div>

      <div v-else-if="recommendationsFetched" class="no-results">
        <p>No recommendations found for this student.</p>
      </div>

      <RouterLink to="/" class="home-link">← Back to Home</RouterLink>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'CourseRecommendation',
  data() {
    return {
      ssn: '',
      recommendedCourses: [],
      recommendationsFetched: false,
    };
  },
  methods: {
    async fetchRecommendations() {
      if (!this.ssn) {
        alert('Please enter a valid SSN.');
        return;
      }

      try {
        const response = await axios.get(`/api/recommend-courses/${this.ssn}`);
        this.recommendedCourses = response.data;
        this.recommendationsFetched = true;
      } catch (error) {
        console.error('Error fetching recommendations:', error);
        alert('Error fetching recommendations. Please check the SSN.');
      }
    },
  },
};
</script>

<style scoped>
.page-container {
  position: relative;
  min-height: 100vh;
  width: 100vw;
  overflow-x: hidden;
  padding: 40px;
  box-sizing: border-box;
}

.background-overlay {
  position: fixed;
  top: 0;
  left: 0;
  z-index: -1;
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  object-position: center;
  pointer-events: none;
}

.logo-top-left {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 200px;
  height: auto;
  z-index: 0;
}

.form-wrapper {
  background-color: rgba(255, 255, 255, 0.95);
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.page-title {
  font-size: 2.5rem;
  color: #006633;
  margin-bottom: 30px;
}

.input-group {
  margin-bottom: 20px;
}

.input-field {
  padding: 10px;
  font-size: 1rem;
  margin-right: 10px;
  width: 250px;
}

.primary-button {
  padding: 10px 20px;
  background-color: #006633;
  color: #ffcc33;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.primary-button:hover {
  background-color: #004d26;
  color: #ffffff;
}

.results {
  margin-top: 30px;
}

.results ul {
  list-style-type: none;
  padding: 0;
}

.results li {
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.no-results {
  margin-top: 20px;
  font-size: 1rem;
  color: #666;
}

.home-link {
  display: block;
  margin-top: 40px;
  color: #006633;
  text-decoration: none;
  font-weight: bold;
}

.home-link:hover {
  text-decoration: underline;
}
</style>
