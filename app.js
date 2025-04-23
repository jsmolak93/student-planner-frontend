const { createApp } = Vue;

createApp({
  data() {
    return {
      studentId: '',
      student: null,
      recommendedCourses: [],
      newStudent: {
        _id: '',
        name: '',
        email: '',
        major: '',
        enrollment_year: '',
        gpa: '',
        eligibleCourses: [],
        degreeGaps: { needed_core: [], needed_electives: [] },
        atRiskStudents: [],
        courseDependency: []
      },
      updatedGPA: ''
    };
  },
  methods: {
    async loadStudentData() {
      try {
        const res = await axios.get(`http://localhost:5000/api/students/${this.studentId}`);
        this.student = res.data;
        const rec = await axios.get(`http://localhost:5000/api/ml/recommend-courses/${this.studentId}`);
        this.recommendedCourses = rec.data.recommended_courses;
      } catch (err) {
        console.error("Error loading student:", err);
      }
    },
    async addStudent() {
      try {
        await axios.post('http://localhost:5000/api/students', this.newStudent);
        alert('Student added!');
      } catch (err) {
        console.error("Error adding student:", err);
      }
    },
    async updateStudentGPA() {
      try {
        await axios.put(`http://localhost:5000/api/students/${this.studentId}`, { gpa: this.updatedGPA });
        alert('GPA updated!');
        this.loadStudentData(); // refresh view
      } catch (err) {
        console.error("Error updating GPA:", err);
      }
    },
    //Query endpoints
    async getEligibleCourses() {
      const res = await axios.get(`http://localhost:5000/api/eligible-courses/${this.studentId}`);
      this.eligibleCourses = res.data.eligible_courses;
    },
    
    async getDegreeGaps() {
      const res = await axios.get(`http://localhost:5000/api/degree-gaps/${this.studentId}`);
      this.degreeGaps = res.data;
    },
    
    async getCourseDependency() {
      const res = await axios.get(`http://localhost:5000/api/course-dependency/${this.student?.major}`);
      this.courseDependency = res.data.recommended_order;
    },
    async getAtRiskStudents() {
      try {
        const res = await axios.get("http://localhost:5000/api/at-risk-students");
        this.atRiskStudents = res.data.at_risk_students;
      } catch (err) {
        console.error("Failed to load at-risk students", err);
      }
    }    
  
  }
  
}).mount('#app');
