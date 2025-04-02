# ISUProjectGrade
# Grade Conversion Web App

This project is a full-stack web application that converts university grades to US-equivalent grade points. It supports multiple country-specific grading formats (e.g., Ghana, China, Nigeria, India).

---

## 🔧 Backend (Flask API)

### 📁 Files
- `app.py`: Main Flask entry point
- `ghana.py`, `china.py`, `nigeria.py`, `india.py`: Country-specific grade lookup logic
- `University List.xlsx`: Excel file containing university mappings and grading formats
- `requirements.txt`: List of Python packages

### ✅ Setup Instructions

```bash
# Clone or copy the project folder
cd CLGPROJ

# (Optional) Create virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
# or
source venv/bin/activate  # Mac/Linux

# Create requirements.txt if not already present
# Or copy-paste the following lines into requirements.txt:
# flask
# pandas
# openpyxl
# flask-cors

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python app.py
```

### 🌐 API Endpoints
- `http://localhost:5000/get_grade_point`
- `http://localhost:5000/get_China_grade_point`
- `http://localhost:5000/get_Nigeria_grade_point`
- `http://localhost:5000/get_India_grade_point`

Each endpoint accepts query parameters:
```
?university=<University Name>&grade=<Grade Value>
```

---

## 💻 Frontend (React UI)

### 📁 Path
- `grade-lookup/`

### 🧪 Steps to Run
```bash
cd grade-lookup
npm install     # Install React dependencies
npm start       # Launch app at http://localhost:3000
```

---

## 📦 What Not to Upload to Git
Add these to `.gitignore`:
```bash
venv/
node_modules/
*.xlsx
```

---

## ✅ Features
- Dynamic format matching per university
- Supports letter grades and numeric ranges
- Handles close matches if exact grade not found
- Organized by country modules for easy extension

---

## 🚀 Next Steps
- Add more countries
- Improve UI responsiveness
- Add error handling and validations in frontend

---

Let me know if you'd like to deploy this online!

