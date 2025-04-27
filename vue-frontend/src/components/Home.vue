<template>
  <div class="home-container">
    <img src="/mason_pond.png" alt="Decorative Background" class="background-overlay" />

    <img src="@/assets/gmulogo.png" alt="GMU Logo" class="logo" />

    <h1>George Mason Student Planner</h1>
    <p class="tagline">Plan your path. Stay on track. Graduate on time.</p>

    <div class="button-group">
      <RouterLink to="/add-student" class="nav-button">Add Student</RouterLink>
      <RouterLink to="/student-planner" class="nav-button">Student Planner</RouterLink>
      <RouterLink to="/course-search" class="nav-button">Course Search</RouterLink>
      <RouterLink to="/course-recommendation" class="nav-button">Course Recommendation</RouterLink>
      <RouterLink to="/analytics" class="nav-button">Analytics</RouterLink>
    </div>
    <div class="bottom-image-wrapper">
      <img src="/mason_graduation.jpg" alt="Mason Graduation" class="bottom-image" />
    </div>
  </div>
</template>

<style scoped>
.home-container {
  position: relative;
  text-align: center;
  padding: 40px;
  background-color: #ffffff;
  overflow: hidden; /* already here — good */
  height: 100vh; /* force full screen height */
}

/* Translucent background image */
.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 60%;
  opacity: 0.15;
  object-fit: cover;
  z-index: 0; /* <-- make it sit at the very back */
}

/* Make all front items sit above the background */
.logo,
h1,
.tagline,
.button-group {
  position: relative;
  z-index: 2; /* <-- bring them forward */
}

/* Logo */
.logo {
  width: 120px;
  margin-bottom: 20px;
}

/* Title */
h1 {
  font-size: 2.5rem;
  color: #006633;
  margin-bottom: 10px;
}

/* Tagline */
.tagline {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 30px;
}

/* Button group */
.button-group {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 40px;
}

.nav-button {
  background-color: #006633;
  color: #ffcc33;
  padding: 12px 24px;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.nav-button:hover {
  background-color: #004d26;
  color: #ffffff;
}

/* Bottom Graduation Image */
.bottom-image-wrapper {
  width: 100vw;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
}

.bottom-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  object-position: center 20%;
  border-radius: 0;
}

</style>
