<template>
    <div class="add-student">
      <h1>Add New Student</h1>
  
      <div class="form">
        <input v-model="student.ssn" placeholder="Student SSN" type="number" />
        <input v-model="student.name" placeholder="Full Name" />
        <input v-model="student.major" placeholder="Major Dcode (e.g., D23)" />
        <select v-model="student.status">
          <option disabled value="">Select Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="">(None)</option>
        </select>
  
        <button @click="addStudent">Add Student</button>
      </div>
  
      <div v-if="message" class="message">
        {{ message }}
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
          const response = await axios.post('/api/students', this.student);
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
  .add-student {
    padding: 20px;
  }
  
  .form {
    display: flex;
    flex-direction: column;
    max-width: 400px;
  }
  
  input, select {
    margin-bottom: 10px;
    padding: 8px;
  }
  
  button {
    align-self: flex-start;
  }
  
  .message {
    margin-top: 15px;
    font-weight: bold;
  }
  </style>
  