# QuestLog 🗡️📜

QuestLog is a gamified task-tracking web application built with **Flask** and **SQLAlchemy** that transforms everyday todos into RPG-style quests. Users complete quests to earn XP, level up, and stay motivated through game-inspired progression mechanics.

---

## 🚀 Live Demo

Check out the deployed app in action:

🔗 https://questlog-pgl4.onrender.com/

Interact with QuestLog, add quests, complete them for XP, and see your level grow!

---

## 🧠 Key Features

- 🎯 Create, edit, and complete quests (tasks)  
- ⭐ Earn XP for completing quests  
- 📈 Automatic level-up system based on your accumulated XP  
- 🔔 Flash messages for instant feedback on actions  
- 🗄️ Persistent data stored via relational database models

---

## 🛠️ Tech Stack

**Backend**  
- Python  
- Flask  
- SQLAlchemy ORM  

**Frontend**  
- HTML  
- CSS  
- Jinja2 templates  

**Deployment**  
- Hosted using Render (or a similar provider)

---

## 🧩 Engineering Challenges

During development, I tackled and solved several non-trivial problems:

### 🔗 Database Relationships  
I designed and implemented relational models using SQLAlchemy to connect users, quests, and progression in a meaningful way.

### ⚡ XP & Leveling Logic  
Built logic that:
- Awards XP when quests are completed  
- Tracks overall XP and calculates when the user levels up

### 📨 Flash Messaging  
Used Flask’s flash system to provide clear, real-time feedback to users for:
- Successful quest adds  
- Quest completion  
- Error handling and invalid input

### 🔄 Flask Architecture  
Organized routes, templates, and models cleanly, improving maintainability and scalability.

---

## 📚 What I Learned

This project helped strengthen my skills in:

- SQLAlchemy ORM and relational database modeling  
- Flask routing and request/response handling  
- Jinja templating for dynamic content  
- Flash message UX patterns  
- Deploying a production-ready web app

---
## 📁 Project Structure
```
QuestLog/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── quest.py
│   ├── quests/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── services.py
│   ├── main/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── quests/
│   │       └── quest_log.html
│   └── static/
│       └── css/
│           └── styles.css
│
├── migrations/      
│
├── config.py
├── run.py
├── requirements.txt
└── README.md

```

## ⚙️ Local Setup

To run this project locally:

```bash
git clone https://github.com/charmythedev/QuestLog.git
cd QuestLog
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python run.py
```

Visit: http://localhost:5000 in your browser

## 🎯 Why This Project Matters

QuestLog is more than a todo list — it demonstrates:

Designing relational database models

Implementing features beyond basic CRUD

Structuring a full-stack Flask application

Deploying an app for real users



