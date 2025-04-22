/// osint_name_search_app (React + FastAPI)
///
/// Folder Structure:
/// - backend/
///     - main.py
///     - .env
///     - requirements.txt
/// - frontend/
///     - src/App.jsx
///     - src/index.js
///     - tailwind.config.js
///     - index.html
///     - package.json

/// ---------------------------
/// 📁 backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BING_API_KEY = os.getenv("BING_API_KEY")
BING_SEARCH_URL = "https://api.bing.microsoft.com/v7.0/search"

class SearchRequest(BaseModel):
    name: str

@app.post("/search")
def search(request: SearchRequest):
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {
        "q": f'"{request.name}" site:linkedin.com OR site:facebook.com OR site:twitter.com OR site:instagram.com OR site:github.com',
        "count": 10
    }

    response = requests.get(BING_SEARCH_URL, headers=headers, params=params)
    data = response.json()

    results = [item["url"] for item in data.get("webPages", {}).get("value", [])]

    return {"results": results}

/// ---------------------------
/// 📁 backend/.env
BING_API_KEY=your_bing_api_key_here

/// ---------------------------
/// 📁 backend/requirements.txt
fastapi
uvicorn
requests
python-dotenv

/// ---------------------------
/// 📁 frontend/src/App.jsx
import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [name, setName] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    const res = await axios.post("http://localhost:8000/search", { name });
    setResults(res.data.results);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">OSINT Name Search</h1>
        <input
          type="text"
          placeholder="Enter name"
          className="w-full p-3 border rounded mb-4"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button
          onClick={handleSearch}
          className="bg-blue-600 text-white px-6 py-2 rounded"
        >
          Search
        </button>

        {loading && <p className="mt-4">Searching...</p>}

        <ul className="mt-6 space-y-2">
          {results.map((link, idx) => (
            <li key={idx} className="bg-white p-3 rounded shadow">
              <a href={link} target="_blank" rel="noopener noreferrer">
                {link}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

/// ---------------------------
/// 📁 frontend/src/index.js
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(<App />);

/// ---------------------------
/// 📁 frontend/tailwind.config.js
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: { extend: {} },
  plugins: [],
};

/// ---------------------------
/// 📁 frontend/index.html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>OSINT Search</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>

/// ---------------------------
/// 📁 frontend/package.json
{
  "name": "osint-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "serve": "vite preview"
  },
  "dependencies": {
    "axios": "^1.6.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "tailwindcss": "^3.3.2",
    "vite": "^4.4.0"
  }
}
