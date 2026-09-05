from app.exceptions import AuthenticationError

from app.schemas.auth_schema import AuthenticatedIdentity

# This is implement together with Entra ID and using MSAL (Micsift supported library
# to handle validation)


def validate_claims(claims):
    entra_object_id = claims.get("oid")
    email = claims.get("email")

    if not entra_object_id:
        raise AuthenticationError("Missing Entra object ID.")

    if not email:
        raise AuthenticationError("Missing email claim.")

    return AuthenticatedIdentity(
        entra_object_id=entra_object_id,
        email=email,
    )


# MOCK Manual Testing;
# - make sure the student testing email exists in SQLite DB first

# Step 1.
# identity = AuthenticatedIdentity(
#     entra_object_id="DEV-ENTRA-001",
#     email="entra.student@example.com",
# )

# Step 2:
# student = resolve_student(identity)

# Step 3:
# Run the app/test_entra_id.py file separately.
# command to run in /backend: python test_entra_id.py and see the output
