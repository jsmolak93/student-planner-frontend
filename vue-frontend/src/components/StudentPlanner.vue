<template>
  <div class="page-container">
    <h1 class="page-title">Student Planner</h1>

    <div class="search-form">
      <input v-model="ssn" placeholder="Enter Student SSN" type="number" required />
      <button @click="loadPlan" class="nav-button">Load Planned Courses</button>
    </div>

    <div class="plan-form">
      <input v-model="newDcode" placeholder="Course Dcode (e.g., D23)" />
      <input v-model="newCno" placeholder="Course Number (e.g., 101)" type="number" />
      <button @click="addCourse" class="nav-button">Add Course to Plan</button>
    </div>

    <div v-if="plannedCourses.length" class="courses-list">
      <h2 class="sub-title">Planned Courses</h2>
      <ul>
        <li v-for="(course, index) in plannedCourses" :key="index" class="course-item">
          <span>{{ course.dcode }} {{ course.cno }}</span>
          <button @click="removeCourse(course.dcode, course.cno)" class="remove-button">
            Remove
          </button>
        </li>
      </ul>
    </div>

    <div v-else-if="searched" class="no-courses">
      No planned courses yet.
    </div>

    <RouterLink to="/" class="home-link">← Back to Home</RouterLink>
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
      if (!this.ssn || !this.newDcode || !this.newCno) {
        alert("Fill in all fields");
        return;
      }
      try {
        await axios.post(`http://localhost:5000/api/students/${this.ssn}/plan`, {
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
        await axios.post(`http://localhost:5000/api/students/${this.ssn}/plan/remove`, {
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
.page-container {
  padding: 40px;
  text-align: center;
  background-color: #ffffff;
  min-height: 100vh;
}

.page-title {
  font-size: 2.5rem;
  color: #006633;
  margin-bottom: 30px;
}

.search-form,
.plan-form {
  max-width: 400px;
  margin: 0 auto 30px;
  display: flex;
  flex-direction: column;
  gap: 15px;
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
}

.sub-title {
  font-size: 1.8rem;
  color: #006633;
  margin-bottom: 20px;
}

.course-item {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
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
