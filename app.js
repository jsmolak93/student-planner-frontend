const { createApp } = Vue;

createApp({
  data() {
    return {
      studentId: '',
      student: null,
      courseSearch: {
        subject: '',
        course_number: '',
        term: ''
      },
      searchedCourse: null,
      newStudent: {
        _id: '',
        name: '',
        email: '',
        major: '',
        gpa: ''
      }
    };
  },

  methods: {
    async addNewStudent() {
      try {
        await axios.post('http://localhost:5000/api/students', this.newStudent);
        alert("Student added!");
      } catch (err) {
        if (err.response?.data?.error === "Student ID already exists") {
          alert("That student ID is already taken.");
        } else {
          alert("Error adding student");
        }
        console.error(err.response?.data || err.message);
      }
    },

    async loadStudent() {
      try {
        const res = await axios.get(`http://localhost:5000/api/students/${this.studentId}`);
        this.student = res.data;
      } catch (err) {
        console.error("Failed to load student:", err);
        alert("Student not found");
      }
    },

    async fetchCourse() {
      try {
        const res = await axios.post(`http://localhost:5000/api/courses/search`, this.courseSearch);

        const [enrollRes, semesterRes] = await Promise.all([
          axios.get(`http://localhost:5000/api/enrollments/count/${res.data.course_id}/${res.data.term}`),
          axios.get(`http://localhost:5000/api/semesters/${res.data.term}`)
        ]);

        this.searchedCourse = {
          ...res.data,
          enrollment_count: enrollRes.data.count,
          start_date: semesterRes.data.start_date,
          end_date: semesterRes.data.end_date
        };
      } catch (err) {
        alert("Course or semester not found");
        this.searchedCourse = null;
        console.error(err.response?.data || err.message);
      }
    },

    async addCourseToPlan() {
      try {
        await axios.post(`http://localhost:5000/api/students/${this.studentId}/plan`, {
          subject: this.courseSearch.subject,
          course_number: this.courseSearch.course_number,
          term: this.courseSearch.term
        });
        await this.loadStudent();
        alert("Course added to plan.");
      } catch (err) {
        console.error("Error adding course:", err);
      }
    },

    async removeCourse(courseId) {
      try {
        await axios.post(`http://localhost:5000/api/students/${this.studentId}/plan/remove`, {
          course_id: courseId
        });
        await this.loadStudent();
      } catch (err) {
        console.error("Error removing course:", err);
      }
    }
  }
}).mount('#app');
