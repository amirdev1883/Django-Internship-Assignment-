# 📝 Mini Task Manager API + Dashboard

A simple task management app built with **Django** and **Django REST Framework** that allows users to:

- Sign up, log in, and log out
- Create, edit, delete, and list tasks
- Manage tasks via both a **web dashboard** and a **REST API**

---

## 🚀 Features

- ✅ User authentication (register, login, logout)
- ✅ Task CRUD operations
- ✅ Dashboard interface for managing tasks
- ✅ REST API endpoints for integration
- ✅ API documentation with Swagger UI

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL (or SQLite for development)  
- **Authentication:** Django built-in authentication  
- **Documentation:** Swagger (drf-yasg)  

---

## 📸 Screenshots (Optional)

![Demo of Task Manager](assets/demo.gif)

---

## ⚙️ Installation & Setup

Clone the repository and set up the environment:

\`\`\`bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
\`\`\`

Visit **http://127.0.0.1:8000/** in your browser.

---

## 📡 API Endpoints

| Method | Endpoint           | Description           |
|-------|------------------|---------------------|
| GET   | \`/api/tasks/\`    | List all tasks      |
| POST  | \`/api/tasks/\`    | Create a new task   |
| PUT   | \`/api/tasks/<id>/\` | Update a task      |
| DELETE| \`/api/tasks/<id>/\` | Delete a task      |

Swagger UI is available at:  
**[\`/swagger/\`](http://127.0.0.1:8000/swagger/)**

---

## 🧪 Running Tests

\`\`\`bash
python manage.py test
\`\`\`


## 🍺 License

This project is licensed under the **Beerware License (Revision 42)**.

> As long as you retain this notice, you can do whatever you want with this stuff.  
> If we meet some day, and you think this stuff is worth it, you can buy me a beer in return. 🍺

