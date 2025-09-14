# 📌 Django Internship Project

## 📖 Project Title  
**Mini Task Manager API + Dashboard**

---

## 🎯 Goal  
Build a simple **task management app** where users can:  

- 🔑 **Sign up & log in**  
- 📝 **Create, edit, delete, and list tasks**  
- 🗓️ Each task has:
  - Title  
  - Description  
  - Due date  
  - Completion status  
- 🌐 Provide **both a web dashboard** and a **REST API** for tasks  

---

## ✅ Requirements  

### 1️⃣ Setup  
- Create a new **Django project** called `taskmanager`  
- Create an app called `tasks`  

---

### 2️⃣ Models  
Create a `Task` model with the following fields:  

| Field        | Type               | Notes |
|-------------|------------------|-------|
| **title**   | `CharField`       |  |
| **description** | `TextField`   | Can be blank |
| **due_date** | `DateField`     |  |
| **completed** | `BooleanField` | `default=False` |
| **owner**   | `ForeignKey` to Django’s `User` |  |

---

### 3️⃣ Authentication  
- Use Django’s **built-in User model**  
- Implement **sign-up** and **login** pages  
- Only logged-in users can manage their own tasks  

---

### 4️⃣ Views & Templates  
Build a dashboard page where a user can:  

- 📋 List their tasks  
- ➕ Create a new task  
- ✅ Mark tasks as completed  
- ��️ Delete tasks  

---

### 5️⃣ REST API (Using DRF)  

| Method | Endpoint | Description |
|-------|-----------|-------------|
| **GET** | `/api/tasks/` | List user’s tasks |
| **POST** | `/api/tasks/` | Create a task |
| **PUT** | `/api/tasks/<id>/` | Update a task |
| **DELETE** | `/api/tasks/<id>/` | Delete a task |

- Use either **SessionAuth** or **TokenAuth** for authentication.  

---

### 6️⃣ Bonus (Optional)  
- 🔍 Add **search & filtering** for tasks  
- 🧪 Write at least **one test case**  
- 🎨 Add a simple **Bootstrap UI**  

---

✨ **This project is a great starting point to practice Django + DRF development, authentication, and basic CRUD operations with a nice UI.**
