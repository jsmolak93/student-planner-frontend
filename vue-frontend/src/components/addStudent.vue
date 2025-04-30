<template>
  <div class="page-with-logo">
    <img src="/mason_logo.png" alt="GMU Background" class="background-overlay" />
    <img src="/mason_mascot.png" alt="Top Left Logo" class="logo-top-left" />
    <div class="form-wrapper">
      <h1 class="page-title">Add New Student</h1>
      <div class="student-form">
        <input v-model="student.ssn" placeholder="Student SSN" type="number" required />
        <input v-model="student.name" placeholder="Full Name" required />
        <input v-model="student.major" placeholder="Major Dcode (e.g., D23)" required />

        <select v-model="student.status">
          <option disabled value="">Select Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="">(None)</option>
        </select>
        <button @click="addStudent" class="nav-button">Add Student</button>
        <!-- Add this inside your .form-wrapper, below the Add Student button -->
        <button @click="deleteStudent" class="nav-button" style="background-color: #cc0000; margin-top: 10px;">
          Delete Student
        </button>

      </div>

      <div v-if="message" class="message">{{ message }}</div>
      <RouterLink to="/" class="home-link">← Back to Home</RouterLink>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AddStudent',
  data() {
    return {
      student: {
        ssn: '',
        name: '',
        major: '',
        status: ''
      },
      message: ''
    };
  },
  methods: {
    async addStudent() {
      if (!this.student.ssn || !this.student.name || !this.student.major) {
        this.message = "SSN, name, and major are required.";
        return;
      }

      try {
        const response = await axios.post('http://localhost:5000/api/students', this.student);
        this.message = response.data.message || "Student added successfully!";
        this.resetForm();
      } catch (error) {
        this.message = error.response?.data?.error || "Error adding student.";
        console.error(error);
      }
    },
    resetForm() {
      this.student = { ssn: '', name: '', major: '', status: '' };
    },
    async deleteStudent() {
      if (!this.student.ssn) {
        this.message = "Please enter the SSN of the student to delete.";
        return;
      }

      try {
        const response = await axios.delete(`http://localhost:5000/api/students/${this.student.ssn}`);
        this.message = response.data.message || "Student deleted successfully.";
        this.resetForm();
      } catch (error) {
        this.message = error.response?.data?.error || "Error deleting student.";
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
.page-with-logo {
  position: relative;
  height: 100vh;
  width: 100vw;
  overflow: hidden; 
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
  margin: 0;
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  object-fit: cover; /* fill entire background area */
  object-position: center;
  z-index: -1;
  pointer-events: none;
}
.logo-top-left {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 200px; /* adjust size as needed */
  height: auto;
  z-index: 1;
}

.form-wrapper {
  background-color: rgba(255, 255, 255, 0.95);
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.page-title {
  font-size: 2.5rem;
  color: #006633;
  margin-bottom: 30px;
}

.student-form {
  display: flex;
  flex-direction: column;
}

input,
select {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
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
  margin-top: 10px;
}

.nav-button:hover {
  background-color: #004d26;
  color: #ffffff;
}

.message {
  margin-top: 20px;
  font-weight: bold;
  color: #333;
}

.home-link {
  display: block;
  margin-top: 30px;
  color: #006633;
  text-decoration: none;
  font-weight: bold;
}

.home-link:hover {
  text-decoration: underline;
}
</style>
