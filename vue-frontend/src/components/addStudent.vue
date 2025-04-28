<template>
  <div class="page-container">
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
    </div>

    <div v-if="message" class="message">{{ message }}</div>

    <RouterLink to="/" class="home-link">← Back to Home</RouterLink>
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
  color: #006633; /* Mason Green */
  margin-bottom: 30px;
}

.student-form {
  max-width: 400px;
  margin: 0 auto;
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
