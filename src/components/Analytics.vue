<template>
    <div>
      <h1>Analytics Dashboard</h1>
      
      <div>
        <h2>Eligible Courses</h2>
        <input v-model="studentId" placeholder="Enter Student ID" />
        <button @click="fetchEligibleCourses">Check Eligibility</button>
        <ul>
          <li v-for="course in eligibleCourses" :key="course">{{ course }}</li>
        </ul>
      </div>
  
      <div>
        <h2>Degree Gaps</h2>
        <button @click="fetchDegreeGaps">Get Degree Gaps</button>
        <p><strong>Core Courses Needed:</strong> {{ degreeGaps.needed_core.join(', ') }}</p>
        <p><strong>Electives Needed:</strong> {{ degreeGaps.needed_electives.join(', ') }}</p>
      </div>
  
      <div>
        <h2>At-Risk Students</h2>
        <button @click="fetchAtRisk">View At-Risk Students</button>
        <ul>
          <li v-for="student in atRisk" :key="student.id">
            {{ student.name }} - GPA: {{ student.gpa }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        studentId: '',
        eligibleCourses: [],
        degreeGaps: {
          needed_core: [],
          needed_electives: []
        },
        atRisk: []
      };
    },
    methods: {
      async fetchEligibleCourses() {
        const res = await axios.get(`http://localhost:5000/api/analytics/eligible-courses/${this.studentId}`);
        this.eligibleCourses = res.data.eligible_courses;
      },
      async fetchDegreeGaps() {
        const res = await axios.get(`http://localhost:5000/api/analytics/degree-gaps/${this.studentId}`);
        this.degreeGaps = res.data;
      },
      async fetchAtRisk() {
        const res = await axios.get('http://localhost:5000/api/analytics/at-risk-students');
        this.atRisk = res.data.at_risk_students;
      }
    }
  };
  </script>
  