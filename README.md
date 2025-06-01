# 🍳 Cooklyst - Recipe Sharing Application

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/devbajaj20/Cooklyst---Recipe-App?style=social)](https://github.com/devbajaj20/Cooklyst---Recipe-App/stargazers)

<div align="center">
  <img src="static/uploads/homepage.png" alt="Cooklyst Homepage" width="800px"/>
</div>

## 📝 Overview

Cooklyst is a modern web application for sharing and discovering recipes, built with Flask and SQLAlchemy. It provides a platform for food enthusiasts to share their culinary creations, discover new recipes, and connect with other food lovers.

## ✨ Features

### 🎯 Core Features
- 🔐 User authentication and profile management
- 📝 Create, edit, and delete recipes
- 🖼️ Upload recipe images
- ⭐ Save favorite recipes
- 🔍 Search and filter recipes
- 👤 User profiles with recipe collections
- 📱 Responsive design for all devices

## 🛠️ Tech Stack

### Backend
- **Python 3.10+** - Core programming language
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database management
- **Flask-Login** - User authentication
- **Flask-Uploads** - File upload handling
- **Flask-Migrate** - Database migrations

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript** - Interactivity
- **Bootstrap** - Responsive design

## 📸 Project Screenshots

### Home Page
<div align="center">
  <img src="static/uploads/homepage.png" alt="Home Page" width="600px"/>
</div>

### My Recipes Page
<div align="center">
  <img src="static/uploads/myrecipespage.png" alt="My Recipes Page" width="600px"/>
</div>

### Progress Tracking
<div align="center">
  <img src="static/uploads/myprogresspage1.png" alt="Progress Page 1" width="600px"/>
  <img src="static/uploads/myprogresspage2.png" alt="Progress Page 2" width="600px"/>
</div>

### User Profile
<div align="center">
  <img src="static/uploads/profilepage.png" alt="User Profile" width="600px"/>
</div>

### Help and Support
<div align="center">
  <img src="static/uploads/helpandsupportpage.png" alt="Help and Support" width="600px"/>
</div>

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/devbajaj20/Cooklyst---Recipe-App.git
cd Cooklyst---Recipe-App
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
python create_tables.py
```

5. **Run the application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
Cooklyst---Recipe-App/
├── app.py              # Main application file
├── models.py           # Database models
├── extensions.py       # Flask extensions
├── create_tables.py    # Database initialization
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, images)
│   ├── css/
│   └── uploads/
└── templates/         # HTML templates
    ├── layout.html
    ├── index.html
    └── ...
```


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

Project Link: [https://github.com/devbajaj20/Cooklyst---Recipe-App](https://github.com/devbajaj20/Cooklyst---Recipe-App)

---

