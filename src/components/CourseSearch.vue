<template>
    <div class="course-search">
      <h1>Course Search</h1>
  
      <div class="filters">
        <input v-model="dcode" placeholder="Department Code (e.g., D23)" />
        <input v-model="cno" placeholder="Course Number (optional)" type="number" />
        <button @click="searchCourses">Search</button>
      </div>
  
      <div class="student-option">
        <input v-model="studentId" placeholder="Student SSN (to enable planner add)" type="number" />
      </div>
  
      <div v-if="results.length" class="results">
        <h2>Search Results</h2>
        <table>
          <thead>
            <tr>
              <th>Dcode</th>
              <th>Cno</th>
              <th>Title</th>
              <th>Units</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(course, index) in results" :key="index">
              <td>{{ course.dcode }}</td>
              <td>{{ course.cno }}</td>
              <td>{{ course.title }}</td>
              <td>{{ course.units }}</td>
              <td>
                <button v-if="studentId" @click="addToPlan(course.dcode, course.cno)">
                  Add to Planner
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <div v-else>
        <p>No results yet.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'CourseSearch',
    data() {
      return {
        dcode: '',
        cno: '',
        studentId: '',
        results: []
      };
    },
    methods: {
      async searchCourses() {
        try {
          // We'll simulate filtering manually since you don’t have a backend filter endpoint yet
          const allCourses = [];
  
          // Pull from each DB and manually filter in frontend
          const dbList = ['univDB1', 'univDB2', 'univDB3', 'univDB4', 'univDB5'];
          for (const db of dbList) {
            const res = await axios.get(`/api/raw/${db}`); // This assumes you set up a /api/raw/:db route
            const courses = res.data?.tables?.course || [];
            allCourses.push(...courses);
          }
  
          this.results = allCourses.filter(course => {
            const matchDcode = !this.dcode || course.dcode === this.dcode;
            const matchCno = !this.cno || course.cno === parseInt(this.cno);
            return matchDcode && matchCno;
          });
        } catch (err) {
          alert("Error searching courses.");
          console.error(err);
        }
      },
      async addToPlan(dcode, cno) {
        try {
          await axios.post(`/api/students/${this.studentId}/plan`, {
            dcode,
            cno
          });
          alert("Course added to planner.");
        } catch (err) {
          alert("Failed to add course.");
          console.error(err);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .course-search {
    padding: 20px;
  }
  .filters, .student-option {
    margin-bottom: 20px;
  }
  input {
    margin-right: 10px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
  }
  th, td {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: left;
  }
  </style>
  