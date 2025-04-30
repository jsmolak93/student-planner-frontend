<template>
  <div class="page-with-logo">
    <img src="/mason_logo.png" alt="GMU Background" class="background-overlay" />
    <img src="/mason_mascot.png" alt="Top Left Logo" class="logo-top-left" />

    <div class="form-wrapper">
      <h1 class="page-title">Student Planner</h1>

      <div class="search-form">
        <input v-model="ssn" placeholder="Enter Student SSN" type="number" required />
        <button @click="loadPlan" class="nav-button">Load Planned Courses</button>
      </div>

      <div class="plan-form">
        <input v-model="newTitle" placeholder="Course Title (e.g., art history)" />
        <input v-model="newCno" placeholder="Course Number (e.g., 101)" type="number" />
        <button @click="addCourse" class="nav-button">Add Course to Plan</button>
      </div>

      <div v-if="plannedCourses.length" class="courses-list">
        <h2 class="sub-title">Planned Courses</h2>
        <ul>
          <li v-for="(course, index) in plannedCourses" :key="index" class="course-item">
            <span>{{ course.title.replace(/_/g, ' ') }} ({{ course.dcode }} {{ course.cno }})</span>
            <button @click="removeCourse(course.dcode, course.cno)" class="remove-button">Remove</button>
          </li>
        </ul>
      </div>

      <div v-else-if="searched" class="no-courses">No planned courses yet.</div>

      <RouterLink to="/" class="home-link">← Back to Home</RouterLink>
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
      plannedCourses: [],
      searched: false
    };
  },
  methods: {
    async loadPlan() {
      if (!this.ssn) {
        alert("Please enter a Student SSN");
        return;
      }
      try {
        const res = await axios.get(`http://localhost:5000/api/students/${this.ssn}/plan`);
        this.plannedCourses = res.data || [];
        this.searched = true;
      } catch (err) {
        alert("Could not load planned courses.");
        console.error(err);
      }
    },
    async addCourse() {
      if (!this.ssn || !this.newTitle || !this.newCno) {
        alert("Fill in all fields");
        return;
      }
      try {
        await axios.post(`http://localhost:5000/api/students/${this.ssn}/plan`, {
          title: this.newTitle.toLowerCase().replace(/\s+/g, "_"),
          cno: parseInt(this.newCno)
        });
        this.loadPlan();
      } catch (err) {
        alert("Error adding course to plan.");
        console.error(err);
      }
    },
        async removeCourse(dcode, cno) {
      try {
        await axios.post(`http://localhost:5000/api/students/${this.ssn}/plan/remove`, {
          dcode,
          cno
        });
        this.loadPlan();
      } catch (err) {
        alert("Error removing course.");
        console.error(err);
      }
    }
  },
  mounted() {
    if (this.ssn) this.loadPlan();
  }
};
</script>

<style scoped>

.page-with-logo {
  position: relative;
  min-height: 100vh;
  width: 100vw;
  background: linear-gradient(to right, #1d5934 50%, #f4c800 50%);
  padding: 40px 0;
  overflow-x: hidden;
  overflow-y: auto;
  z-index: 0;
  display: flex;
  justify-content: center;
  align-items: flex-start;
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
  z-index: 1;
}

.form-wrapper {
  background-color: rgba(255, 255, 255, 0.95);
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  text-align: center;
  max-width: 600px;
  width: 100%;
}

.page-title {
  font-size: 2.5rem;
  color: #006633;
  margin-bottom: 30px;
}

.search-form,
.plan-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
}

input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

.nav-button {
  background-color: #006633;
  color: #ffcc33;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.nav-button:hover {
  background-color: #004d26;
  color: #ffffff;
}

.courses-list {
  margin-top: 30px;
  text-align: left;
}

.sub-title {
  font-size: 1.8rem;
  color: #006633;
  margin-bottom: 20px;
  text-align: center;
}

.course-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
}

.remove-button {
  background-color: #cc0000;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 0.9rem;
  cursor: pointer;
}

.remove-button:hover {
  background-color: #990000;
}

.no-courses {
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
