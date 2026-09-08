To start the application (for testing):
Run this command to create Database tables and include mock data:
`python seed_db.py`
Then run command:
`flask --app backend.app:create_app --debug run` to run the application on localhost