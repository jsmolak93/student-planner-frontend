<template>
    <div class="planner">
      <h1>Student Planner</h1>
  
      <div class="inputs">
        <input v-model="ssn" placeholder="Enter Student SSN" type="number" />
      </div>
  
      <div class="actions">
        <button @click="loadPlan">Load Planned Courses</button>
      </div>
  
      <div class="plan-form">
        <input v-model="newDcode" placeholder="Course Dcode (e.g., D23)" />
        <input v-model="newCno" placeholder="Course Number (e.g., 101)" type="number" />
        <button @click="addCourse">Add Course to Plan</button>
      </div>
  
      <div class="results" v-if="plannedCourses.length">
        <h2>Planned Courses</h2>
        <ul>
          <li v-for="(course, index) in plannedCourses" :key="index">
            {{ course.dcode }} {{ course.cno }}
            <button @click="removeCourse(course.dcode, course.cno)">Remove</button>
          </li>
        </ul>
      </div>
  
      <div v-else>
        <p>No planned courses yet.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'StudentPlanner',
    props: ['studentId'],
    data() {
      return {
        ssn: this.studentId || '',
        newDcode: '',
        newCno: '',
        plannedCourses: []
      };
    },
    methods: {
      async loadPlan() {
        if (!this.ssn) {
          alert("Please enter a Student SSN");
          return;
        }
        try {
          const res = await axios.get(`/api/students/${this.ssn}/plan`);
          this.plannedCourses = res.data;
        } catch (err) {
          alert("Could not load planned courses.");
          console.error(err);
        }
      },
      async addCourse() {
        if (!this.ssn || !this.newDcode || !this.newCno) {
          alert("Fill in all fields");
          return;
        }
        try {
          await axios.post(`/api/students/${this.ssn}/plan`, {
            dcode: this.newDcode,
            cno: parseInt(this.newCno)
          });
          this.loadPlan(); // Refresh
        } catch (err) {
          alert("Error adding course to plan.");
          console.error(err);
        }
      },
      async removeCourse(dcode, cno) {
        try {
          await axios.post(`/api/students/${this.ssn}/plan/remove`, {
            dcode: dcode,
            cno: cno
          });
          this.loadPlan(); // Refresh
        } catch (err) {
          alert("Error removing course.");
          console.error(err);
        }
      }
    },
    mounted() {
      if (this.ssn) {
        this.loadPlan();
      }
    }
  };
  </script>
  
  <style scoped>
  .planner {
    padding: 20px;
  }
  
  .inputs, .actions, .plan-form {
    margin-bottom: 20px;
  }
  
  input {
    margin-right: 10px;
  }
  
  button {
    margin-right: 10px;
  }
  </style>
  