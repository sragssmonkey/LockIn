# Lock In — Smart Study & Auto-Quiz Platform

Lock In is a full-stack web platform designed to help students study with focus and get automated quizzes based on the content they upload or read.  
It is built using Django (Python), HTML, Tailwind CSS, and Vanilla JavaScript.

---

## 🚀 Features
- User login & authentication  
- Focused study mode  
- Automatic quiz generation  
- PDF upload & content extraction  
- Personalized quiz dashboard  
- Progress tracking  

---

## 🛠️ Tech Stack
- **Backend:** Django (Python)  
- **Frontend:** HTML, Tailwind CSS, JavaScript  
- **Database:** SQLite / PostgreSQL  

---

## 📦 Installation & Setup

Follow these steps to run the project locally:

### 1️⃣ Clone the Repository
```bash
git clone <your-repository-link>
cd lockin
```
2. Create a Virtual Environment
```bash
python -m venv env
```
Activate it:
Windows:
```bash
env\Scripts\activate
```
Mac / Linux:
```bash
source env/bin/activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
5. Apply Migrations
```bash
python manage.py migrate
```
7. Run the Server
```bash
python manage.py runserver
```
Visit the app at:
http://127.0.0.1:8000/

🔑 Environment Variables (Optional)
Create a .env file if needed:
SECRET_KEY=your_django_secret_key
DEBUG=True
API_KEY=xxxx





