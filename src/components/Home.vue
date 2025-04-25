<template>
  <div class="home">
    <header>
      <img src="@/assets/gmu-logo.png" alt="GMU Logo" />
      <h1>George Mason Student Planner</h1>
    </header>

    <section class="intro">
      <p>📚 Plan your path. ✅ Stay on track. 🎓 Graduate on time.</p>
      <p>This student planner helps you manage your courses, visualize your progress, and meet graduation goals.</p>
    </section>

    <section class="nav-buttons">
      <router-link to="/add-student"><button>Add Student</button></router-link>
      <router-link to="/planner"><button>Course Planner</button></router-link>
      <router-link to="/course-search"><button>Search Courses</button></router-link>
      <router-link to="/analytics"><button>Analytics</button></router-link>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home'
};
</script>

<style scoped>
:root {
  --gmu-green: #006633;
  --gmu-gold: #ffcc33;
  --gmu-white: #ffffff;
  --gmu-dark: #333;
}

.home {
  text-align: center;
  padding: 40px;
  font-family: 'Segoe UI', sans-serif;
  background-color: var(--gmu-white);
  color: var(--gmu-dark);
}

header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  border-bottom: 4px solid var(--gmu-green);
  padding-bottom: 20px;
}

header img {
  height: 80px;
}

h1 {
  color: var(--gmu-green);
  font-size: 32px;
  margin: 0;
}

.intro {
  margin: 30px auto;
  max-width: 600px;
  font-size: 18px;
  color: #444;
}

.nav-buttons {
  margin-top: 40px;
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

button {
  background-color: var(--gmu-green);
  color: var(--gmu-white);
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.2s ease-in-out;
}

button:hover {
  background-color: var(--gmu-gold);
  color: var(--gmu-dark);
}
</style>
