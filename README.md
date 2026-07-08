# Library Management System

A production-ready REST API built using **FastAPI** and **Pydantic** to handle CRUD operations for a library system.

## Features
* **Create**: Add new books with input validation.
* **Read**: Fetch all books or pull specific records by ID.
* **Update**: Perform partial or complete book detail modifications.
* **Delete**: Remove books cleanly from the system database.

## How to Run Locally
1. Install requirements:
   ```bash
   python -m pip install fastapi uvicorn pydantic
   ```
2. Start the local development server:
   ```bash
   python -m uvicorn main:app --reload
   ```
3. Open the interactive API documentation at `http://127.0.0`.
