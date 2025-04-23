<template>
    <div class="home">
      <h1>Welcome to the Student Course Planner</h1>
      <p>Use the navigation above or click a button below to get started.</p>
  
      <router-link to="/add-student">
        <button>Add New Student</button>
      </router-link>
      <router-link to="/search">
        <button>Search Courses</button>
      </router-link>
      <router-link to="/analytics">
        <button>View Analytics</button>
      </router-link>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Home'
  }
  </script>
  
  <style scoped>
  .home {
    text-align: center;
    margin-top: 2rem;
  }
  button {
    margin: 0.5rem;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
  }
  </style>
  