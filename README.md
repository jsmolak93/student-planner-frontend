# Student Planner Web App

A full-stack web application for managing university students and their course plans. Built with Vue.js and Flask, connected via RESTful APIs using Axios, and backed by MongoDB.

## Technologies Used

**Frontend:**
- Vue.js (Vite)
- Axios

**Backend:**
- Python
- Flask
- Flask-CORS
- PyMongo

**Database:**
- MongoDB


## Setup Instructions (Mac/Linux/Windows)

### 1. Clone the Project

```bash
git https://github.com/jsmolak93/student_planner/tree/refactored-planner
cd student_planner
```

### 2. Set Up Backend (Flask)

```bash
cd planner-backend
python3 -m venv venv         
source venv/bin/activate    
pip install -r ../requirements.txt
```

Ensure MongoDB is running locally on default port (27017).  

### 3. Set Up Frontend (Vue)

```bash
cd ../vue-frontend
npm install
```

### 4. Run Both Servers Concurrently

In the root folder:

```bash
npm install
npm run dev
```

This uses the `concurrently` package to start both backend and frontend servers.


## Backend Python Requirements

Generated via `pip freeze`:

```
blinker==1.9.0
click==8.1.8
colorama==0.4.6
dnspython==2.7.0
Flask==3.1.0
flask-cors==5.0.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
pymongo==4.12.1
Werkzeug==3.1.3
```



## Notes

- Courses and students are stored in MongoDB collections.
- Axios is used to bridge the Vue frontend with the Flask API.
- Student Planner supports adding/removing courses, searching by department or number, and tracking planned courses.


## Author
John Smolak
Mostafa Omidi