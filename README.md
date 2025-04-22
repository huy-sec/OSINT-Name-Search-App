# OSINT-Name-Search-App
Search names on popular social media sites

🔐 Setup
Get a Bing Search API key from Azure.

Add .env file with your API key:

bash
Copy
Edit
BING_API_KEY=your_bing_key_here
Run backend:

bash
Copy
Edit
uvicorn main:app --reload
Connect frontend to backend (localhost:8000/search).

🧪 To Run It Locally
🔹 Backend
bash
Copy
Edit
cd backend
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload

Make sure you’ve added your BING_API_KEY in .env.

🔹 Frontend
bash
Copy
Edit
cd frontend
npm install
npm run dev
