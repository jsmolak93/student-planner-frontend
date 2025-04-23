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
        gpa: ''
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
    }
  }
  
}).mount('#app');
