# ISUProjectGrade
For Windows (assumed):
If you're using Mac/Linux, let me know and I'll tailor the steps.

📦 Install:
Install Python (e.g., 3.10 or higher)

Download: https://www.python.org/downloads/

Make sure to check ✅ Add Python to PATH during install!

Install Git

Download: https://git-scm.com/downloads

Install Node.js (for frontend React app)

Download: https://nodejs.org/

This will install node and npm (Node Package Manager)

✅ Step 2: Clone Your GitHub Repo
bash
Copy
Edit
git clone https://github.com/Sinhaamisha5/ISUProjectGrade.git
cd ISUProjectGrade
✅ Step 3: Set Up & Run the Backend (Flask)
1. Go into your backend folder:
(If it's all in root, skip this step)

bash
Copy
Edit
cd backend-folder-name  # or stay in root if backend is here
2. Create a virtual environment (optional but recommended):
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On Mac/Linux
3. Install required Python packages:
bash
Copy
Edit
pip install -r requirements.txt
4. Run the Flask app:
bash
Copy
Edit
python app.py
This should start your Flask API on:
http://localhost:5000

✅ Step 4: Set Up & Run the Frontend (React App)
1. Go into your frontend folder:
bash
Copy
Edit
cd grade-lookup  # Assuming that's your React folder
2. Install frontend dependencies:
bash
Copy
Edit
npm install
3. Start the frontend:
bash
Copy
Edit
npm start
Your React app will open in the browser at
http://localhost:3000
