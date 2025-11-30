# 📄 Bill Extractor AI – FastAPI + OCR + Gemini

Automated system to extract item-level bill details from PDF invoices, using OCR + Google Gemini AI, built with FastAPI, fully containerized using Docker, tested using pytest, and deployed on Render.

## 🚀 Features
Feature	Description
🧾 PDF Upload	Accepts invoice PDFs via API
🔍 OCR Processing	Uses Tesseract + pdf2image
🤖 AI Parsing	Gemini LLM structures item data
📦 JSON Response	Returns extracted name, qty, cost
🧪 Pytest Integrated	CI-ready test suite
🐳 Dockerized	Production-ready image
🌍 Live Public Link	Deployable on Render / EC2 / Jenkins
🔗 Live Demo
Resource	URL
Swagger UI	https://bajaj-finserv-t1ze.onrender.com/docs

Base URL	https://bajaj-finserv-t1ze.onrender.com
📁 Project Structure
```
📦 Bill-Extractor-AI
├── main.py              # FastAPI entry point
├── extractor.py         # OCR + Gemini processing logic
├── requirements.txt
├── Dockerfile
├── tests/
│   └── test_main.py     # pytest API test
└── README.md
```

⚙ Installation & Setup (Local)
```
git clone https://github.com/Saketh2611/Bajaj-Finserv
cd Bajaj-Finserv
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit UI →
http://localhost:8000/docs

🐳 Run With Docker
```
docker build -t bill-extractor-api .
docker run -d -p 8000:8000 bill-extractor-api
```

🧪 Run Tests (pytest)
pytest


✔ Tests are already configured in CI
✔ Validates FastAPI response & JSON output

🧠 API Usage
POST /extract
curl -X POST "https://bajaj-finserv-t1ze.onrender.com/extract" \
-F "file=@invoice.pdf"

Response Example
```
{
  "store": "D-Mart",
  "date": "2025-02-12",
  "items": [
    { "name": "Oil", "qty": 1, "price": 120 },
    { "name": "Chips", "qty": 3, "price": 30 }
  ],
  "total": 210
}
```

🏗 Deployment (Render)
Build Command     →  ```pip install -r requirements.txt```
Start Command     →  ```uvicorn main:app --host 0.0.0.0 --port 8000```


Upload repository → Deploy → Access public URL 🎉

📌 Future Improvements
Planned Feature	Benefit
DB Storage	Save invoice history
Multi-page support	Ideal for supermarket bills
Fine-tuned invoice LLM	Higher accuracy
Web dashboard UI	Visual analysis
✨ Author

Vaddiparthi Saketh — IIT Madras