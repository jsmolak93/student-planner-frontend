<template>
  <div class="page-container">
    <img src="/mason_logo.png" alt="Background" class="background-overlay" />
    <img src="/mason_mascot.png" alt="GMU Logo" class="logo-top-left" />

    <div class="form-wrapper">
      <h1 class="page-title">Course Search</h1>

      <div class="filters">
        <input v-model="dcode" placeholder="Department Code (e.g., D23)" />
        <input v-model="cno" placeholder="Course Number (optional)" type="number" />
        <button @click="searchCourses" class="nav-button">Search Courses</button>
      </div>

      <div class="student-option">
        <input v-model="studentId" placeholder="Student SSN (to enable adding to planner)" type="number" />
      </div>

      <div v-if="results.length" class="results">
        <h2 class="sub-title">Search Results</h2>
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
                <button v-if="studentId" @click="addToPlan(course.dcode, course.cno)" class="small-button">
                  Add to Planner
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else-if="searched" class="no-results">
        No results found.
      </div>

      <RouterLink to="/" class="home-link">← Back to Home</RouterLink>
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
      results: [],
      searched: false
    };
  },
  methods: {
      async searchCourses() {
        try {
          const response = await axios.get('/api/courses');
          const allCourses = response.data || [];

          this.results = allCourses.filter(course => {
            const matchDcode = !this.dcode || course.dcode === this.dcode;
            const matchCno = !this.cno || course.cno === parseInt(this.cno);
            return matchDcode && matchCno;
          });
          this.searched = true;
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
  width: 200px;  /* Try increasing */
  height: auto;
  z-index: 0;
}


.page-container {
  padding: 40px;
  text-align: center;
  min-height: 100vh;
  background: linear-gradient(to right, #1d5934 50%, #f4c800 50%); /* GMU green & gold split */
  position: relative;
  z-index: 0;
}

.page-title {
  font-size: 2.5rem;
  color: #006633;
  margin-bottom: 30px;
}

.form-wrapper {
  background-color: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  text-align: center;
  max-width: 700px; /* Reduce from 900px or 100% */
  width: 90%;
  margin: 0 auto;
}

.filters, .student-option {
  margin-bottom: 20px;
}

input {
  margin: 10px;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

.nav-button {
  background-color: #006633;
  color: #ffcc33;
  padding: 10px 20px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.nav-button:hover {
  background-color: #004d26;
  color: #ffffff;
}

.results {
  margin-top: 30px;
}

.sub-title {
  font-size: 1.8rem;
  color: #006633;
  margin-bottom: 20px;
}

table {
  width: 100%;
  margin-top: 15px;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ccc;
  padding: 12px;
  text-align: center;
}

th {
  background-color: #006633;
  color: #ffffff;
}

.small-button {
  background-color: #006633;
  color: #ffcc33;
  padding: 5px 10px;
  border-radius: 6px;
  border: none;
  font-size: 0.9rem;
}

.small-button:hover {
  background-color: #004d26;
  color: #ffffff;
}

.no-results {
  margin-top: 30px;
  font-size: 1.2rem;
  color: #333;
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
