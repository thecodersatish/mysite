# 🧑‍💻 Online Programming Courses Platform

An interactive **online learning platform** built with **Python (Django Framework)** where students can **learn programming languages** like **C, C++, Python, and Java** through **video tutorials, quizzes (MCQs), hands-on coding exercises**, and **module-wise assessments**.

---

## 🚀 Features

- 🎥 **Video Lessons** — Learn each topic through structured video modules.  
- 🧠 **MCQs and Quizzes** — Test understanding after each lesson.  
- 💻 **Hands-On Coding** — Write and execute code directly on the platform.  
- 📝 **Assessments** — Module-wise tests to evaluate student performance.  
- 👨‍🎓 **Student Enrollment System** — Register and enroll in multiple programming courses.  
- 🧾 **Progress Tracking** — Students can view completed modules and scores.  
- 🔒 **Secure Authentication** — Login and signup system using Django authentication.  

---

## 🏗️ Tech Stack

| Category | Technology |
|-----------|-------------|
| **Backend** | Python, Django |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap |
| **Database** | SQLite / MySQL (configurable) |
| **Version Control** | Git, GitHub |
| **Editor/IDE** | VS Code / PyCharm |

---

## 📁 Project Structure
online_courses/
│
├── courses/ # App for course management
├── users/ # App for user authentication and profiles
├── lessons/ # App for videos, MCQs, coding modules
├── assessments/ # App for quizzes and evaluation
├── static/ # Static assets (CSS, JS, images)
├── templates/ # HTML templates
├── manage.py
└── requirements.txt

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/thecodersatish/mysite.git
   cd mysite

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate     # On Windows  
   source venv/bin/activate  # On Mac/Linux  

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
5. **Apply migrations**
   ```bash
   python manage.py migrate
6. **Run the development server**
   ```bash
   python manage.py runserver

Open your browser and go to: http://127.0.0.1:8000/
