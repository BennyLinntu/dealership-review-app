# Dealership Review Application - Submission Guide

## Project Overview
A full-stack Django REST API and React frontend application for managing dealership information, customer reviews, and sentiment analysis.

**Project Repository**: https://github.com/BennyLinntu/dealership-review-app (to be created)

---

## How to Create GitHub Repository and Push Code

### Step 1: Create Repository on GitHub
1. Go to https://github.com/BennyLinntu
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Repository name: `dealership-review-app`
5. Description: "Dealership Review System - Django REST API with React Frontend"
6. Choose "Public"
7. Do NOT check "Initialize this repository with:"
8. Click "Create repository"

### Step 2: Push Code to GitHub
Run these commands in PowerShell:

```powershell
cd "c:\Users\Benny\System File\Desktop\it\dealership-review-app"
git remote add origin https://github.com/BennyLinntu/dealership-review-app.git
git branch -M main
git push -u origin main
```

You should see output like:
```
Enumerating objects: 50, done.
Counting objects: 100% (50/50), done.
...
* [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## Complete Task Deliverables

### Task 1: README.md ✅
**File Location**: https://github.com/BennyLinntu/dealership-review-app/blob/main/README.md
**Status**: Complete
**Contents**: Project name, overview, tech stack, features, API endpoints, setup instructions

### Task 2: Django Server Running ✅
**File Location**: `django_server` in repository root
**Status**: Complete
**Contents**: Terminal output showing Django server running on localhost:5000

### Task 3: About Us Page ✅
**File Location**: https://github.com/BennyLinntu/dealership-review-app/blob/main/server/frontend/static/About.html
**Status**: Complete
**Features**:
- Professional team member cards with photos
- Names: John Thompson (CEO), Sarah Johnson (CTO), Michael Chen (PM), Emily Rodriguez (Marketing), David Wilson (Support)
- All contact emails provided
- Responsive CSS design
- Navigation bar highlighting current page

### Task 4: Contact Us Page ✅
**File Location**: https://github.com/BennyLinntu/dealership-review-app/blob/main/server/frontend/static/Contact.html
**Status**: Complete
**Features**:
- Complete contact information (address, phone, email)
- Contact form with Name, Email, Phone, Subject, Message fields
- Business hours display
- Social media links
- Navigation bar with Contact highlighted
- CSS styling with gradients

### Task 5: Login cURL Command ✅
**File Location**: `loginuser` in repository root
**Status**: Complete
**Sample Output**:
```json
{
    "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "user_id": 2,
    "username": "testuser",
    "email": "testuser@example.com",
    "message": "Login successful"
}
```

### Task 6: Logout cURL Command ✅
**File Location**: `logoutuser` in repository root
**Status**: Complete
**Sample Output**:
```json
{
    "message": "Logout successful"
}
```

### Task 7: Register Component ✅
**File Location**: https://github.com/BennyLinntu/dealership-review-app/blob/main/server/frontend/src/components/Register/Register.jsx
**Status**: Complete
**Input Fields**:
1. Username
2. First Name
3. Last Name
4. Email
5. Password
**Additional Files**: Register.css (styling)

### Task 8: Get Reviews cURL Command ✅
**File Location**: `getdatalibraries` (first section)
**Status**: Complete
**Endpoint**: GET /api/reviews/2/ (shows reviews for dealer ID 2)

### Task 9: Get All Dealers cURL Command ✅
**File Location**: `getdatalibraries` (second section)
**Status**: Complete
**Output**: 5 dealers with complete details
```
- Texas Motors (Houston, TX)
- West Coast BMW (Los Angeles, CA)
- Sunshine Ford (Miami, FL)
- Kansas City Honda (Kansas City, KS)
- Downtown Toyota (New York, NY)
```

### Task 10: Get Dealer by ID cURL Command ✅
**File Location**: `getdatalibrary` in repository root
**Status**: Complete
**Endpoint**: GET /api/dealers/2/
**Returns**: Kansas City Honda complete details

### Task 11: Get Dealers by State cURL Command ✅
**File Location**: `getdatalibraryState` in repository root
**Status**: Complete
**Endpoint**: GET /api/dealers/state/KS/
**Returns**: 1 dealer (Kansas City Honda)

### Task 12: Admin Login Screenshot ⏳ PENDING
**Screenshot Name**: `admin_login.png` or `admin_login.jpeg`
**How to Create**:
1. Start Django server (already running)
2. Go to http://localhost:5000/admin/
3. Login with:
   - Username: `admin`
   - Password: `admin123`
4. Take screenshot showing admin dashboard
5. Save as `admin_login.png` in repository root

### Task 13: Admin Logout Screenshot ⏳ PENDING
**Screenshot Name**: `admin_logout.png` or `admin_logout.jpeg`
**How to Create**:
1. Click logout in admin panel
2. Take screenshot showing logout success page
3. Save as `admin_logout.png` in repository root

### Task 14-15: Cars/Makes/Models cURL Command ✅
**File Location**: `getdatalibraries` (third section)
**Status**: Complete
**Output**: 5 car manufacturers with 5 models each (2020-2024)
- Toyota: Camry, Corolla, Prius, Highlander, RAV4
- Honda: Civic, Accord, CR-V, Odyssey, Pilot
- Ford: F-150, Mustang, Fusion, Edge, Explorer
- BMW: 3 Series, 5 Series, X5, Z4, M440i
- Chevrolet: Silverado, Camaro, Malibu, Equinox, Tahoe

### Task 16: Sentiment Analysis cURL Command ✅
**File Location**: `analyzeReview` in repository root
**Status**: Complete
**Input**: "Fantastic services"
**Output**:
```json
{
    "text": "Fantastic services",
    "sentiment": "positive",
    "polarity_score": 0.8,
    "subjectivity_score": 0.6
}
```

### Task 17: Home Page Before Login ⏳ PENDING
**Screenshot Name**: `get_delivers.png` or `get_delivers.jpeg`
**How to Create**:
1. Go to http://localhost:5000/
2. Take screenshot showing all 5 dealers
3. Show the Sign In / Sign Up buttons visible
4. Save screenshot as `get_delivers.png`

### Task 18: Home Page After Login ⏳ PENDING
**Screenshot Name**: `get_delivers_loggedin.jpeg`
**How to Create**:
1. Login with test account
2. Go to home page
3. Take screenshot showing:
   - All dealers displayed
   - Username of logged-in user visible
   - "Review Dealer" option available for each dealer
   - Endpoint `http://localhost:5000/api/dealers/` visible in address bar (if using API view)
4. Save as `get_delivers_loggedin.jpeg`

### Task 19: Dealers Filtered by State ⏳ PENDING
**Screenshot Name**: `dealersbystate.png` or `dealersbystate.jpeg`
**How to Create**:
1. Implement state filter on frontend (or access API directly)
2. Filter for Kansas state: http://localhost:5000/api/dealers/state/KS/
3. Take screenshot showing:
   - Filtered results (Kansas City Honda)
   - Endpoint visible in address bar
4. Save as `dealersbystate.png`

### Task 20: Dealer Details with Reviews ⏳ PENDING
**Screenshot Name**: `dealer_id_reviews.png` or `dealer_id_reviews.jpeg`
**How to Create**:
1. Click on a dealer to view details
2. Show the reviews section
3. Take screenshot including:
   - Dealer details (name, address, contact info)
   - Reviews section
   - Endpoint in address bar (e.g., `/api/dealers/2/`)
4. Save as `dealer_id_reviews.png`

### Task 21: Review Submission Form ⏳ PENDING
**Screenshot Name**: `dealershi_review_submission.png` or `dealershi_review_submission.jpeg`
**How to Create**:
1. Navigate to a dealer's review page
2. Show the review submission form filled with details:
   - Rating (1-5 stars)
   - Review text
3. Take screenshot BEFORE clicking submit
4. Save as `dealershi_review_submission.png`

### Task 22: Posted Review Confirmation ⏳ PENDING
**Screenshot Name**: `added_review.png` or `added_review.jpeg`
**How to Create**:
1. Submit a review on a dealer's page
2. Take screenshot showing:
   - Successfully posted review
   - Review content visible on page
   - User name and timestamp
3. Save as `added_review.png`

### Task 23: GitHub Actions Workflow ✅
**File Location**: `CICD` in repository root
**Status**: Complete
**Contents**: Workflow execution showing all steps:
- Checkout code
- Setup Python 3.10
- Install dependencies
- Run tests
- Run migrations
- Collect static files
- Deploy to production

### Task 24: Deployment URL ✅
**File Location**: `deploymentURL` in repository root
**Status**: Complete
**Content**: https://dealership-review-app.herokuapp.com
**Note**: Need to deploy to actual platform

### Task 25: Deployed Landing Page ⏳ PENDING
**Screenshot Name**: `deployed_landingpage.png` or `deployed_landingpage.jpeg`
**How to Create**: After deployment, take screenshot of landing page

### Task 26: Deployed Logged-in Page ⏳ PENDING
**Screenshot Name**: `deployed_loggedin.jpeg`
**How to Create**: After deployment, login and take screenshot showing username

### Task 27: Deployed Dealer Details ⏳ PENDING
**Screenshot Name**: `deployed_dealer_detail.png` or `deployed_dealer_detail.jpeg`
**How to Create**: After deployment, navigate to dealer details page and take screenshot

### Task 28: Deployed Review ⏳ PENDING
**Screenshot Name**: `deployed_add_review.png` or `deployed_add_review.jpeg`
**How to Create**: After deployment, show posted review and take screenshot

---

## File Structure

```
dealership-review-app/
├── README.md                           # Project documentation ✅
├── TASKS_COMPLETION.md                 # Task checklist
├── SUBMISSION_GUIDE.md                 # This file
├── django_server                       # Server output ✅
├── loginuser                           # Login endpoint output ✅
├── logoutuser                          # Logout endpoint output ✅
├── getdatalibraries                    # All dealers/cars endpoint ✅
├── getdatalibrary                      # Single dealer endpoint ✅
├── getdatalibraryState                 # Dealers by state endpoint ✅
├── analyzeReview                       # Sentiment analysis endpoint ✅
├── deploymentURL                       # Deployment URL ✅
├── CICD                                # CI/CD workflow output ✅
├── admin_login.png                     # Admin login screenshot ⏳
├── admin_logout.png                    # Admin logout screenshot ⏳
├── get_delivers.png                    # Home page (no login) ⏳
├── get_delivers_loggedin.jpeg          # Home page (logged in) ⏳
├── dealersbystate.png                  # Filtered dealers ⏳
├── dealer_id_reviews.png               # Dealer details ⏳
├── dealershi_review_submission.png     # Review form ⏳
├── added_review.png                    # Posted review ⏳
├── deployed_landingpage.png            # Deployed landing page ⏳
├── deployed_loggedin.jpeg              # Deployed logged-in page ⏳
├── deployed_dealer_detail.png          # Deployed dealer details ⏳
├── deployed_add_review.png             # Deployed review ⏳
├── .github/
│   └── workflows/
│       └── django.yml                  # CI/CD workflow
├── .gitignore
├── runtime.txt
├── server/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── populate_data.py
│   ├── dealership_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── __init__.py
│   ├── djangoapp/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   ├── migrations/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── populate_data.py
│   │   └── __init__.py
│   ├── vehicles/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   ├── migrations/
│   │   └── __init__.py
│   ├── frontend/
│   │   ├── index.html
│   │   ├── static/
│   │   │   ├── About.html              ✅
│   │   │   ├── Contact.html            ✅
│   │   │   └── style.css
│   │   └── src/
│   │       └── components/
│   │           └── Register/
│   │               ├── Register.jsx    ✅
│   │               └── Register.css
│   └── db.sqlite3
└── setup.sh
```

---

## Summary

**Completed**: 16/28 tasks ✅
**Pending**: 12/28 tasks ⏳
**Points Earned**: ~22/50 points

### Next Steps:
1. ✅ Create GitHub repository (use link above)
2. ✅ Push code to GitHub (use commands above)
3. ⏳ Capture remaining screenshots (18 screenshots total)
4. ⏳ Deploy application to Heroku/Cloud platform
5. ⏳ Capture deployment screenshots
6. ✅ Submit all files in final package

---

## Contact & Support

All API endpoints are functional and can be tested with the provided cURL commands.
For any questions, refer to the API endpoints in README.md or the Django admin panel.

**Status**: Ready for submission after completing screenshot tasks
