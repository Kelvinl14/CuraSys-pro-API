# CuraSys-pro-API

CuraSys-pro API is a robust backend system designed with a clean MVC architecture. It leverages modern technologies such as Flask, PostgreSQL, Docker, and WSGI to provide a scalable and maintainable solution for managing medical consultations, exams, and user authentication.



## **Project Structure**

The project follows the MVC (Model-View-Controller) architecture:

```bash
CuraSys-pro-API/
├── app/
│   ├── controllers/       # Business logic for handling requests
│   ├── models/            # Database models (SQLAlchemy ORM)
│   ├── routes/            # API routes (Flask Blueprints)
│   ├── extensions.py      # Extensions (e.g., database, migrations)
│   ├── __init__.py        # App factory
├── migrations/            # Database migration files
├── tests/                 # Unit and integration tests
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose for multi-container setup
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md              # Project documentation
```

---

## **Technologies Used**

- **Python**: Backend programming language.
- **Flask**: Web framework for building the API.
- **PostgreSQL**: Relational database for storing data.
- **SQLAlchemy**: ORM for database interaction.
- **Docker**: Containerization for consistent environments.
- **WSGI (Gunicorn)**: Production-ready server.
- **Pytest**: Testing framework.

---

## **Setup Instructions**

Follow these steps to set up and run the project:

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/CuraSys-pro-API.git
cd CuraSys-pro-API
```

### **2. Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure Environment Variables**
Create a `.env` file in the root directory with the following content:
```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/curasys
SECRET_KEY=your_secret_key
```

### **5. Run Database Migrations**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### **6. Run the Application**
```bash
flask run
```

The API will be available at `http://localhost:5000`.

---

## **Using Docker**

### **1. Build the Docker Image**
```bash
docker-compose build
```

### **2. Start the Containers**
```bash
docker-compose up
```

The API will be available at `http://localhost:5000`.

---

## **Main Features**

### **1. User Authentication**
- **Hashing Passwords**: Securely store user passwords using `bcrypt`.
- **Endpoints**:
  - `POST /users`: Create a new user.
  - `POST /login`: Authenticate a user.

### **2. Medical Consultations**
- **CRUD Operations**:
  - `GET /consultas`: List all consultations.
  - `GET /consultas/<id>`: Retrieve a specific consultation.
  - `POST /consultas`: Create a new consultation.
  - `PUT /consultas/<id>`: Update an existing consultation.
  - `DELETE /consultas/<id>`: Delete a consultation.

### **3. Exams**
- **CRUD Operations**:
  - `GET /exames`: List all exams.
  - `GET /exames/<id>`: Retrieve a specific exam.
  - `POST /exames`: Create a new exam.
  - `PUT /exames/<id>`: Update an existing exam.
  - `DELETE /exames/<id>`: Delete an exam.
- **File Upload**:
  - `POST /exames/<id>/upload`: Upload a file for an exam.

### **4. Patient and Doctor Management**
- **Endpoints**:
  - `GET /paciente/<id>/consultas`: List all consultations for a specific patient.
  - `GET /medico/<id>/consultas`: List all consultations for a specific doctor.

---

## **Testing**

Run the test suite using `pytest`:
```bash
pytest
```

---

## **Contributing**

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
```
