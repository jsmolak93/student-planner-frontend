<template>
  <div class="analytics">
    <h1>Analytics</h1>

    <div class="inputs">
      <input v-model="studentId" placeholder="Enter Student SSN" type="number" />
      <input v-model="majorDcode" placeholder="Enter Major Dcode (e.g., D11)" />
    </div>

    <div class="buttons">
      <button @click="fetchEligibleCourses">Find Eligible Courses</button>
      <button @click="fetchDegreeRequirements">Find Degree Requirements</button>
      <button @click="fetchAtRiskStudents">Find At-Risk Students</button>
      <button @click="fetchCourseDependency">Show Course Dependency</button>
    </div>

    <div class="results" v-if="results.length">
      <h2>Results</h2>
      <ul>
        <li v-for="(item, index) in results" :key="index">
          {{ item }}
        </li>
      </ul>
    </div>

    <div v-else>
      <p>No results yet. Please run a query.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Analytics',
  data() {
    return {
      studentId: '',
      majorDcode: '',
      results: []
    };
  },
  methods: {
    async fetchEligibleCourses() {
      if (!this.studentId) {
        alert("Please enter a Student SSN");
        return;
      }
      const response = await axios.get(`/api/eligible-courses/${this.studentId}`);
      this.results = response.data;
    },
    async fetchDegreeRequirements() {
      if (!this.studentId) {
        alert("Please enter a Student SSN");
        return;
      }
      const response = await axios.get(`/api/degree-requirements/${this.studentId}`);
      this.results = response.data;
    },
    async fetchAtRiskStudents() {
      const response = await axios.get(`/api/at-risk-students`);
      this.results = response.data;
    },
    async fetchCourseDependency() {
      if (!this.majorDcode) {
        alert("Please enter a Major Dcode");
        return;
      }
      const response = await axios.get(`/api/course-dependency/${this.majorDcode}`);
      this.results = response.data.course_order || [];
    }
  }
};
</script>

<style scoped>
.analytics {
  padding: 20px;
}
.inputs {
  margin-bottom: 20px;
}
.buttons {
  margin-bottom: 20px;
}
.results {
  margin-top: 30px;
}
button {
  margin-right: 10px;
}
</style>
