# Cooklyst - Recipe Sharing Application

A modern web application for sharing and discovering recipes, built with Flask and SQLAlchemy.

## Features

- User authentication and profile management
- Create, edit, and delete recipes
- Upload recipe images
- Save favorite recipes
- Search and filter recipes
- User profiles with recipe collections
- Responsive design for all devices

## Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **File Upload**: Flask-Uploads
- **Database Migrations**: Flask-Migrate

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/devbajaj20/Cooklyst---Recipe-App.git
cd Cooklyst---Recipe-App
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python create_tables.py
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

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

## Features in Detail

### User Management
- User registration and login
- Profile customization
- Password management

### Recipe Management
- Create new recipes with images
- Edit existing recipes
- Delete recipes
- View recipe details

### Social Features
- Save favorite recipes
- View other users' profiles
- Browse recipe collections

### Search and Filter
- Search recipes by name
- Filter by categories
- Sort by various criteria

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter)

Project Link: [https://github.com/devbajaj20/Cooklyst---Recipe-App](https://github.com/devbajaj20/Cooklyst---Recipe-App)