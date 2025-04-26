<template>
    <div class="recommendation-container">
      <h1>Course Recommendations</h1>
  
      <div class="input-group">
        <label for="ssn">Enter Student SSN:</label>
        <input type="number" id="ssn" v-model="ssn" placeholder="Enter SSN..." />
        <button @click="fetchRecommendations">Get Recommendations</button>
      </div>
  
      <div v-if="recommendedCourses.length > 0" class="recommendations">
        <h2>Recommended Courses:</h2>
        <ul>
          <li v-for="course in recommendedCourses" :key="`${course.dcode}-${course.cno}`">
            {{ course.dcode }} {{ course.cno }} - {{ course.title }}
          </li>
        </ul>
      </div>
  
      <div v-else-if="recommendationsFetched">
        <p>No recommendations found for this student.</p>
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
        recommendationsFetched: false
      };
    },
    methods: {
      async fetchRecommendations() {
        try {
          const response = await axios.get(`http://localhost:5000/api/recommend-courses/${this.ssn}`);
          this.recommendedCourses = response.data;
          this.recommendationsFetched = true;
        } catch (error) {
          console.error('Error fetching recommendations:', error);
          alert('Error fetching recommendations. Please check the SSN.');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .recommendation-container {
    padding: 20px;
    background-color: #f9f9f9;
  }
  
  .input-group {
    margin-bottom: 20px;
  }
  
  input[type="number"] {
    margin: 0 10px;
    padding: 5px;
  }
  
  button {
    padding: 5px 10px;
    background-color: #006633; /* GMU green */
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #004d26; /* Darker GMU green */
  }
  
  .recommendations ul {
    list-style-type: none;
    padding: 0;
  }
  </style>
  