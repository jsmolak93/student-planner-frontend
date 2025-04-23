const { createApp } = Vue;

createApp({
  data() {
    return {
      studentId: '',
      student: null,
      planner: {
        subject: '',
        course_number: '',
        term: ''
      },
      latestPlannedCourse: null,
      allPlannedCourses: [],
      editTerm: ''
    };
  },
  methods: {
    async loadStudentData() {
      try {
        const res = await axios.get(`http://localhost:5000/api/students/${this.studentId}`);
        this.student = res.data;
        this.loadAllPlannedCourses();
      } catch (err) {
        console.error("Error loading student:", err);
      }
    },
    async submitPlanner() {
      try {
        const res = await axios.post(`http://localhost:5000/api/students/${this.studentId}/plan`, this.planner);
        this.latestPlannedCourse = res.data;
        alert('Course planned successfully!');
        this.loadAllPlannedCourses();
      } catch (err) {
        console.error("Error submitting planner info:", err);
      }
    },
    async loadAllPlannedCourses() {
      try {
        const res = await axios.get(`http://localhost:5000/api/students/${this.studentId}/plan`);
        this.allPlannedCourses = res.data.planned_courses;
      } catch (err) {
        console.error("Error loading planned courses:", err);
      }
    },
    async deletePlannedCourse(courseId) {
      try {
        await axios.post(`http://localhost:5000/api/students/${this.studentId}/plan/delete`, {
          course_id: courseId
        });
        alert('Course removed from planner');
        this.loadAllPlannedCourses();
      } catch (err) {
        console.error("Error deleting course:", err);
      }
    },
    async updateCourseTerm(courseId, newTerm) {
      try {
        await axios.put(`http://localhost:5000/api/students/${this.studentId}/plan/update`, {
          course_id: courseId,
          new_term: newTerm
        });
        alert('Course term updated');
        this.loadAllPlannedCourses();
      } catch (err) {
        console.error("Error updating course term:", err);
      }
    }
  }
}).mount('#app');