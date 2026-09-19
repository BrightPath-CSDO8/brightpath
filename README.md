To start testing of backend endpoints (in Development), run these commands in sequence:
1. Ensure virtual environment is activated
2. `cd backend`
3. `pip install -r requirements.txt` 
4. `python seed_db.py`
This create SQLite tables and include initial mock data.
5. `python -m backend.run` 
This command starts backend application.
6. Navigate to endpoints (E.g. `/api/v1/courses`)
