
# CareerBridge 🎓

**CareerBridge** is a full-featured Django-based web application built for college placement cells.  
It helps admins manage company recruitment drives and allows students to view, apply to, and track job/internship opportunities.

---

## 🚀 Features

### 👨‍🏫 Admin
- Secure login
- Add, update, delete company details
- Upload details like company type, positions, skills, packages, interview dates, etc.

### 🎓 Student
- Register and login
- View all active companies
- Search by name, location, skills
- Apply to roles or withdraw applications
- See applied companies with interview alerts
- Export company and application data to Excel

### 📊 General
- Role-based access
- Mobile responsive UI (Bootstrap 5)
- Company detail page with full info + PDF links
- Alerts for interviews within 2 days
- Excel download for:
  - All companies
  - Applied companies

---

## 🛠 Tech Stack

| Layer        | Tech                         |
|--------------|------------------------------|
| Backend      | Django 5.x                   |
| Database     | SQLite (easy to migrate)     |
| Frontend     | HTML, Bootstrap 5            |
| Export       | OpenPyXL (for Excel support) |
| Auth         | Django built-in auth system  |

---

## 📁 Folder Structure

````
CareerBridge/
├── accounts/         # User login/register
├── placement/        # Core app: companies, applications
├── templates/        # All templates: base, auth, placement
├── static/           # CSS, JS, Images (if needed)
├── db.sqlite3        # Default DB
├── manage.py
└── README.md

````

---

## 🧑‍💻 Getting Started (Local)

1. Clone the repo

```bash
git clone https://github.com/yourusername/CareerBridge.git
cd CareerBridge
````

2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run migrations

```bash
python manage.py migrate
```

5. Create superuser

```bash
python manage.py createsuperuser
```

6. Start server

```bash
python manage.py runserver
```

---


## 📌 Future Enhancements

* Email notifications for interview dates
* Resume upload for students
* Shortlist status per company
* Admin dashboard with analytics

---

## 📸 Screenshots (Optional)

> You can upload screenshots and add links here once UI is finalized.

---


**Built with ❤️ for student career success**

