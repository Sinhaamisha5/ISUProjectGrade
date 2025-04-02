# ISUProjectGrade
# Grade Conversion Web App

This project is a full-stack web application that converts university grades to US-equivalent grade points. It supports multiple country-specific grading formats (e.g., Ghana, China, Nigeria, India).

---

## Backend (Flask API)

### Files
- `app.py`: Main Flask entry point
- `ghana.py`, `china.py`, `nigeria.py`, `india.py`: Country-specific grade lookup logic
- `University List.xlsx`: Excel file containing university mappings and grading formats
- `requirements.txt`: List of Python packages

### Setup Instructions

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

###  API Endpoints
- `http://localhost:5000/get_grade_point`
- `http://localhost:5000/get_China_grade_point`
- `http://localhost:5000/get_Nigeria_grade_point`
- `http://localhost:5000/get_India_grade_point`

Each endpoint accepts query parameters:
```
?university=<University Name>&grade=<Grade Value>
```

---

##  Frontend (React UI)

###  Path
- `grade-lookup/`

###  Steps to Run
```bash
cd grade-lookup
npm install     # Install React dependencies
npm start       # Launch app at http://localhost:3000
```

---

## What Not to Upload to Git
Add these to `.gitignore`:
```bash
venv/
node_modules/
*.xlsx
```

---

##  Features
- Dynamic format matching per university
- Supports letter grades and numeric ranges
- Handles close matches if exact grade not found
- Organized by country modules for easy extension

---

##  Next Steps
- Add more countries
- Improve UI responsiveness
- Add error handling and validations in frontend

---

---------------
Installation steps

# Grade Equivalency Lookup System

A full-stack web application to fetch **US grade point equivalents** for universities in **Ghana**, **China**, and **Nigeria** using Excel-based grading formats.

---

##  Project Structure
```
clgproj/                   # Project Root
├── app.py                # Flask backend entry point
├── ghana.py              # Ghana grade logic
├── china.py              # China grade logic
├── nigeria.py            # Nigeria grade logic
├── University List.xlsx  # Excel data file (excluded from Git)
└── grade-lookup/         # React frontend app
```

---

##  Backend Setup (Flask)

### 1. Install Dependencies
```bash
pip install flask flask-cors pandas openpyxl
```

### 2. Run Flask Server
```bash
python app.py
```
> Flask runs at: `http://localhost:5000`

### API Endpoints:
| Endpoint                                | Country  |
|----------------------------------------|----------|
| `/get_grade_point`                     | Ghana    |
| `/get_China_grade_point`               | China    |
| `/get_Nigeria_grade_point`             | Nigeria  |

---

## Frontend Setup (React)

### 1. Initialize React App
```bash
cd grade-lookup
npm install
```

### 2. Run React Server
```bash
npm start
```
> React runs at: `http://localhost:3000`

### Features:
- Buttons to select **country**
- Input fields for **University** and **Grade**
- Result display with **US GPA equivalents**

---

## Packages Used

### Backend:
| Package      | Purpose                          |
|--------------|----------------------------------|
| `flask`      | Web server framework             |
| `flask-cors` | Enable frontend-backend requests |
| `pandas`     | Excel file reading               |
| `openpyxl`   | `.xlsx` file engine              |

### Frontend:
| Tool         | Purpose                          |
|--------------|----------------------------------|
| `react`      | UI framework                     |
| `fetch API`  | API requests                     |

---

## Notes
- **Excel File** (`University List.xlsx`) is **excluded from Git**.
- Excel sheets must include:
  - `Ghana University List`, `Ghana Formats`
  - `China University List`, `China Formats`
  - `Nigeria University List`, `Nigeria Formats`
- Special grades like `A+` should be URL-encoded as `A%2B`.

---

# Grade Conversion Web App

This project is a full-stack web application that converts university grades to US-equivalent grade points. It supports multiple country-specific grading formats (e.g., Ghana, China, Nigeria, India).

---

## Backend (Flask API)

### Files
- `app.py`: Main Flask entry point
- `ghana.py`, `china.py`, `nigeria.py`, `india.py`: Country-specific grade lookup logic
- `University List.xlsx`: Excel file containing university mappings and grading formats
- `requirements.txt`: List of Python packages

### Setup Instructions

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

### API Endpoints
- `http://localhost:5000/get_grade_point`
- `http://localhost:5000/get_China_grade_point`
- `http://localhost:5000/get_Nigeria_grade_point`
- `http://localhost:5000/get_India_grade_point`

Each endpoint accepts query parameters:
```
?university=<University Name>&grade=<Grade Value>
```

---

## Frontend (React UI)

### Path
- `grade-lookup/`

### Steps to Run
```bash
cd grade-lookup
npm install     # Install React dependencies
npm start       # Launch app at http://localhost:3000
```

---

##  What Not to Upload to Git
Add these to `.gitignore`:
```bash
venv/
node_modules/
*.xlsx
```

---

## Features
- Dynamic format matching per university
- Supports letter grades and numeric ranges
- Handles close matches if exact grade not found
- Organized by country modules for easy extension

---

## Next Steps
- Add more countries
- Improve UI responsiveness
- Add error handling and validations in frontend

---

Let me know if you'd like to deploy this online!



---

## 👩‍💻 Author
Developed by **Amisha Sinha**

Let me know if you need help deploying, debugging, or expanding this project! 🚀


