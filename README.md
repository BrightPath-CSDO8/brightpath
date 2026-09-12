# BrightPath

BrightPath is an education management platform.

## Database

The application uses Azure SQL Database.

### Azure SQL

Server:
brightpath-sql-server.database.windows.net

Database:
brightpath-db

Authentication:
Microsoft Entra ID

### Database Models

The database contains the following tables:

- Users
- Student
- Teacher
- Admin
- Classroom
- Course
- Enrolment
- Attendance
- Grade

### Local Development

Install the Python dependencies:

pip install -r database/requirements.txt

Microsoft ODBC Driver 18 for SQL Server must also be installed on the
developer's machine.

The local Azure SQL connection uses Microsoft Entra device-code
authentication.

Test the connection with:

python database/test_sqlalchemy_connection.py

The connection includes retry logic because the serverless Azure SQL
database may take time to resume after being idle.

### Role-Based Access

The Users table contains a role field with:

- student
- teacher
- admin

The backend should use this role after Microsoft Entra authentication
to authorize API operations.

### Production

DeviceCodeCredential is intended for local development.

For deployment to Azure, the backend should use a non-interactive
identity such as Azure Managed Identity with DefaultAzureCredential.