<template>
  <div class="recommendation-container">
    <h1>Course Recommendations</h1>

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
.recommendation-container {
  padding: 30px;
  background-color: #ffffff;
  text-align: center;
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
  background-color: #006633; /* GMU Green */
  color: #ffcc33; /* GMU Gold */
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.primary-button:hover {
  background-color: #004d26; /* Darker GMU green */
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

</style>
