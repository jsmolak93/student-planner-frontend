<template>
  <div class="analytics-container">
    <h1>Student Analytics</h1>

    <div class="input-group">
      <input
        v-model="studentId"
        type="number"
        placeholder="Enter Student SSN (for eligibility/recommendation)"
        class="input-field"
      />
      <input
        v-model="majorDcode"
        type="text"
        placeholder="Enter Major Dcode (for dependency, e.g., D11)"
        class="input-field"
      />
    </div>

    <div class="button-group">
      <button @click="fetchEligibleCourses" class="primary-button">Find Eligible Courses</button>
      <button @click="fetchDegreeRequirements" class="primary-button">Find Degree Requirements</button>
      <button @click="fetchAtRiskStudents" class="primary-button">Find At-Risk Students</button>
      <button @click="fetchCourseDependency" class="primary-button">Show Course Dependency</button>
      <button @click="fetchInstructorWorkload" class="primary-button">Instructor Workload</button>
      <button @click="fetchStudentUnits" class="primary-button">Units Per Student</button>

    </div>

    <div v-if="results.length > 0" class="results">
      <h2>Results</h2>

      <table v-if="results[0]?.risk_courses !== undefined" class="analytics-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>SSN</th>
            <th>Major</th>
            <th>Risk Courses</th>
          </tr>
        </thead>
        <tbody>
          <tr 
              v-for="(item, index) in results" 
              :key="index"
              :class="{
                'dark-red-row': item.risk_courses >= 3,
                'medium-orange-row': item.risk_courses === 2,
                'light-yellow-row': item.risk_courses === 1
              }"
            >
            <td>{{ item.name }}</td>
            <td>{{ item.ssn }}</td>
            <td>{{ item.major }}</td>
            <td :class="{ 'high-risk': item.risk_courses >= 3 }">
              {{ item.risk_courses }}
            </td>
          </tr>
        </tbody>
      </table>

      <table v-else-if="results[0]?.instructor !== undefined" class="analytics-table">
        <thead>
          <tr>
            <th>Instructor</th>
            <th>Courses Taught</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in results" :key="index">
            <td>{{ row.instructor }}</td>
            <td>{{ row.count }}</td>
          </tr>
        </tbody>
      </table>

      <table v-else-if="results[0]?.progress !== undefined" class="analytics-table">
        <thead>
          <tr>
            <th>Student Name</th>
            <th>SSN</th>
            <th>Major</th>
            <th>Courses Completed</th>
            <th>Total Required</th>
            <th>Progress (%)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in results" :key="index">
            <td>{{ row.name }}</td>
            <td>{{ row.ssn }}</td>
            <td>{{ row.major }}</td>
            <td>{{ row.completed }}</td>
            <td>{{ row.required }}</td>
            <td>{{ row.progress }}</td>
          </tr>
        </tbody>
      </table>

      <table v-else-if="results[0]?.dcode && results[0]?.cno" class="analytics-table">
        <thead>
          <tr>
            <th>Department Code</th>
            <th>Course Number</th>
            <th>Title</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(course, index) in results"
            :key="index"
            :class="{ 'highlight-major': course.dcode === studentMajor }"
          >
            <td>{{ course.dcode }}</td>
            <td>{{ course.cno }}</td>
            <td>{{ course.title }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Instructor Workload Table -->
      <table v-else-if="results[0]?.courses_taught !== undefined" class="analytics-table">
        <thead>
          <tr>
            <th>Instructor Name</th>
            <th>Courses Taught</th>
            <th>Course Titles</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in results" :key="index">
            <td>{{ item.name }}</td>
            <td>{{ item.courses_taught }}</td>
            <td>{{ item.courses.join(', ') }}</td>
          </tr>
        </tbody>
      </table>



      <!-- Student Units Table -->
      <table v-else-if="results[0]?.units !== undefined" class="analytics-table">
        <thead>
          <tr>
            <th>Student Name</th>
            <th>SSN</th>
            <th>Units Completed</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in results" :key="index">
            <td>{{ item.name }}</td>
            <td>{{ item.ssn }}</td>
            <td>{{ item.units }}</td>
          </tr>
        </tbody>
      </table>


      <ul v-else>
        <li v-for="(item, index) in results" :key="index">
          {{ item }}
        </li>
      </ul>
    </div>

    <div v-else-if="queryExecuted" class="no-results">
      <p>No results found. Please run a query.</p>
    </div>
    <RouterLink to="/" class="home-link">← Back to Home</RouterLink>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Analytics',
  data() {
    return {
      studentId: '',
      majorDcode: '',
      studentMajor: '',
      results: [],
      queryExecuted: false,
    };
  },
  methods: {
    async fetchEligibleCourses() {
      if (!this.studentId) {
        alert("Please enter a Student SSN");
        return;
      }
      try {
        const response = await axios.get(`/api/eligible-courses/${this.studentId}`);
        this.results = response.data.courses || [];
        this.studentMajor = response.data.major || '';
        this.queryExecuted = true;
      } catch (error) {
        console.error('Error fetching eligible courses:', error);
        alert('Failed to fetch eligible courses.');
      }
    },

    async fetchDegreeRequirements() {
      if (!this.studentId) {
        alert("Please enter a Student SSN");
        return;
      }
      try {
        const response = await axios.get(`/api/recommend-courses/${this.studentId}`);
        this.results = response.data;
        this.queryExecuted = true;
      } catch (error) {
        console.error('Error fetching degree requirements:', error);
        alert('Failed to fetch degree requirements.');
      }
    },

    async fetchAtRiskStudents() {
      try {
        const response = await axios.get(`/api/at-risk-students`);
        this.results = response.data;
        this.queryExecuted = true;
      } catch (error) {
        console.error('Error fetching at-risk students:', error);
        alert('Failed to fetch at-risk students.');
      }
    },

    async fetchCourseDependency() {
      if (!this.majorDcode) {
        alert("Please enter a Major Dcode");
        return;
      }
      try {
        const response = await axios.get(`/api/course-dependency/${this.majorDcode}`);
        this.results = response.data.course_order || [];
        this.studentMajor = response.data.major.dname || '';
        this.queryExecuted = true;
      } catch (error) {
        console.error('Error fetching course dependencies:', error);
        alert('Failed to fetch course dependencies.');
      }
    },

    async fetchInstructorWorkload() {
      try {
        const response = await axios.get('/api/instructor-workload');
        this.results = response.data.map(item => ({
          ...item,
          courses: item.courses.map(title =>
            title
              .replace(/_/g, ' ')
              .replace(/\b\w/g, char => char.toUpperCase()) 
          )
        }));
        this.queryExecuted = true;
      } catch (error) {
        console.error('Error fetching instructor workload:', error);
        alert('Failed to fetch instructor workload.');
      }
    },

    async fetchStudentUnits() {
      try {
        const response = await axios.get('/api/student-units');
        this.results = response.data.map(item => ({
          name: item.name
            .replace(/_/g, ' ')
            .replace(/\b\w/g, char => char.toUpperCase()),
          ssn: item.ssn,
          units: item.units
        }));
        this.queryExecuted = true;
      } catch (error) {
        console.error('Error fetching student units:', error);
        alert('Failed to fetch student units.');
      }
    },
  },
};
</script>


<style scoped>
.analytics-container {
  padding: 30px;
  background-color: #ffffff;
  text-align: center;
}

.input-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.input-field {
  padding: 10px;
  font-size: 1rem;
  width: 250px;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-bottom: 30px;
}

.primary-button {
  padding: 10px 20px;
  background-color: #006633; /* GMU Green */
  color: #ffcc33; /* GMU Gold */
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.primary-button:hover {
  background-color: #004d26; /* Darker Mason Green */
  color: #ffffff;
}

.results {
  margin-top: 30px;
}

.results ul {
  list-style: none;
  padding: 0;
}

.results li {
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.no-results {
  margin-top: 20px;
  font-size: 1rem;
  color: #666;
}
.home-link {
  display: block;
  margin-top: 40px;
  color: #006633;
  text-decoration: none;
  font-weight: bold;
}
.analytics-table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

.analytics-table th, .analytics-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
}

.analytics-table th {
  background-color: #006633; /* Mason Green */
  color: #ffffff;
}

.analytics-table td {
  background-color: #f9f9f9;
}

.analytics-table tr:hover td {
  background-color: #e6ffe6; /* light green hover effect */
}

.dark-red-row {
  background-color: #ffcccc; /* light red background */
  color: #990000; /* dark red text */
  font-weight: bold;
}

.medium-orange-row {
  background-color: #ffd8a8; /* medium orange background */
  color: #cc5500; /* deeper orange text */
  font-weight: bold;
}

.light-yellow-row {
  background-color: #fffff0; /* ultra-light yellow, almost white-yellow */
  color: #d0d001; /* a little softer and more readable */
  font-weight: bold;
}

.highlight-major {
  background-color: transparent;
  color: #006633;
  font-weight: bold;
}


</style>
