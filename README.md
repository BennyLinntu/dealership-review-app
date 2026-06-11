# xrwvm-fullstack_developer_capstone

## Repository Name

**xrwvm-fullstack_developer_capstone** — GitHub Repository: [BennyLinntu/dealership-review-app](https://github.com/BennyLinntu/dealership-review-app)

## Project Name

**fullstack_developer_capstone** — A full-stack Django and React application for managing dealership information, customer reviews, and sentiment analysis.

## Overview

This application allows users to:

- Browse and search for dealerships
- View detailed dealership information
- Submit and view reviews with sentiment analysis
- Manage user authentication and profiles
- Filter dealers by state and other criteria
- View car makes and models

## Tech Stack

- **Backend**: Django REST Framework
- **Frontend**: React.js
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: Django Token-based Authentication
- **Sentiment Analysis**: Python TextBlob
- **Deployment**: Cloud Platform
- **CI/CD**: GitHub Actions

## Features

### Backend API

- Dealer Management API
- Review Management API
- Car Makes and Models API
- User Authentication (Login/Logout/Register)
- Sentiment Analysis API
- State-based Dealer Filtering

### Frontend

- Responsive HTML/CSS Pages
- React Components for User Registration
- About Us Page
- Contact Us Page
- Dealer Listing and Details
- Review Submission and Display

## Project Structure

```
dealership-review-app/
├── server/
│   ├── manage.py
│   ├── dealership_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── models.py
│   ├── frontend/
│   │   ├── static/
│   │   │   ├── About.html
│   │   │   ├── Contact.html
│   │   │   └── style.css
│   │   └── src/
│   │       └── components/
│   │           └── Register/
│   │               └── Register.jsx
│   └── requirements.txt
└── README.md
```

## Installation & Setup

### Backend Setup

```bash
cd server
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup

```bash
npm install
npm start
```

## API Endpoints

- `GET /api/dealers/` - Get all dealers
- `GET /api/dealers/<id>/` - Get dealer details
- `GET /api/dealers/state/<state>/` - Get dealers by state
- `GET /api/reviews/<dealer_id>/` - Get reviews for a dealer
- `POST /api/reviews/` - Post a new review
- `GET /api/cars/` - Get all car makes and models
- `POST /api/sentiment/` - Analyze review sentiment
- `POST /api/login/` - User login
- `POST /api/logout/` - User logout
- `POST /api/register/` - User registration

## Authentication

The application uses Django Token-based authentication. Include the token in the Authorization header:

```
Authorization: Token <your_token>
```

## Author

BennyLinntu

## License

MIT License
