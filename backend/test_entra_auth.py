from app import create_app

from app.schemas.auth_schema import AuthenticatedIdentity
from app.auth.service import resolve_student

app = create_app()

with app.app_context():

    identity = AuthenticatedIdentity(
        entra_object_id="DEV-ENTRA-001",
        email="entra-student-dev@example.com",
    )

    # identity = {
    #     "entra_object_id": "DEV-ENTRA-001",
    #     "email": "entra-student-dev@example.com",
    # }

    test_student = resolve_student(identity)

    print(f"Test Entra Student: {test_student}")
