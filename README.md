To start the application (for testing):
Run this command to create Database tables and include mock data:
`python seed_db.py`
Then run command:
`flask --app backend.app:create_app --debug run --host=localhost --port=5001` to run the application on localhost