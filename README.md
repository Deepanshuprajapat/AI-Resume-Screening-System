# 🧠 AI Resume Screening System

An intelligent web-based application that automates the recruitment process by analyzing resumes and matching them with job descriptions using Natural Language Processing (NLP) and Machine Learning techniques.

---

## 🚀 Features

* 📄 Upload resumes (PDF format)
* 🧠 Extract resume text automatically
* 🎯 Match resumes with job descriptions
* 📊 Generate similarity score (ranking candidates)
* 🧾 Create and manage job postings
* 📌 Display ranked candidates for each job

---

## 🏗️ Tech Stack

### 🔹 Backend

* Python
* Flask
* SQLAlchemy
* Scikit-learn (TF-IDF + Cosine Similarity)

### 🔹 Frontend

* HTML
* CSS
* JavaScript (Vanilla JS)

### 🔹 NLP / Parsing

* PDFMiner (for resume parsing)
* TF-IDF Vectorization

---

## 📁 Project Structure

```
project/
│
├── app.py                # Main Flask app
├── config.py            # Configuration settings
├── models.py            # Database models
├── matcher.py           # Resume-job matching logic
├── resume_parser.py     # Resume parsing logic
│
├── static/
│   ├── js/app.js
│   └── css/style.css
│
├── templates/
│   └── index.html
│
└── data/
    ├── app.db
    └── resumes/
```

---

## ⚙️ How It Works

1. User creates a job posting with required skills.
2. Candidate uploads resume.
3. Resume text is extracted using PDF parsing.
4. System calculates similarity score using TF-IDF + Cosine Similarity.
5. Candidates are ranked based on match score.

👉 Matching logic implemented in:

* matcher.py → 
* resume parsing → 

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/resume-screening.git
cd resume-screening
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install dependencies

```bash
pip install flask flask-cors flask-sqlalchemy scikit-learn pdfminer.six
```

---

### 4️⃣ Run the application

```bash
python app.py
```

👉 Backend runs on:

```
http://127.0.0.1:5000
```

👉 Health check endpoint:

*

---

### 5️⃣ Open Frontend

Open:

```
index.html
```

---

## 📊 API Endpoints

| Method | Endpoint                  | Description           |
| ------ | ------------------------- | --------------------- |
| GET    | /api/health               | Check server status   |
| GET    | /api/jobs                 | Get all jobs          |
| POST   | /api/jobs                 | Create new job        |
| POST   | /api/candidates/upload    | Upload resume         |
| GET    | /api/jobs/{id}/candidates | Get ranked candidates |

---

## 🧠 Database Models

Defined in:

*

### Entities:

* **Job**
* **Candidate**

---

## 🔍 Matching Algorithm

* TF-IDF Vectorization
* Cosine Similarity

👉 Implemented in:

*

---

## 💡 Future Improvements

* 🔥 Advanced NLP using NLTK / SpaCy
* 📈 Better skill extraction
* 📎 Support DOCX resumes
* 👤 Authentication system
* 📊 Dashboard analytics

---

## 🧑‍💻 Author

**Deepanshu Prajapati**

---

## 📜 License

This project is for educational purposes.

---

## ⭐ GitHub Tip

If you like this project, give it a ⭐ on GitHub!
