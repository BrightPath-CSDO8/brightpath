from flask import Blueprint, request, jsonify, current_app, session, redirect
import msal
import json
from urllib.parse import urlencode
from urllib.request import urlopen

from sqlalchemy.exc import IntegrityError
from backend.app.extensions import db
from pydantic import ValidationError

# from app.models.users import User
from database.models import Users

# Schemas
from backend.app.schemas.user_schema import StudentCreate, StudentResponse, StaffCreate
from backend.app.schemas.auth_schema import LoginRequest

# Service
from backend.app.services.user_service import svc_register_student, svc_register_staff
from backend.app.services.auth_service import svc_login

# Exceptions
from backend.app.exceptions.auth import EmailAlreadyRegisteredError, AuthenticationError

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1")


# MSAL helper
def build_msal_app():
    return msal.ConfidentialClientApplication(
        client_id=current_app.config["ENTRA_AZURE_CLIENT_ID"],
        authority=current_app.config["AUTHORITY"],
        client_credential=current_app.config["ENTRA_AZURE_CLIENT_SECRET"],
    )


# Checks Flask <--> Entra ID connection
@auth_bp.route("/auth/entra-test", methods=["GET"])
def entra_test():
    tenant_id = current_app.config["ENTRA_AZURE_TENANT_ID"]

    metadata_url = (
        f"https://login.microsoftonline.com/"
        f"{tenant_id}/v2.0/.well-known/openid-configuration"
    )

    try:
        with urlopen(metadata_url, timeout=5) as response:
            metadata = json.load(response)

        return jsonify(
            {
                "status": "success",
                "message": "Successfully connected to Microsoft Entra ID",
                "issuer": metadata.get("issuer"),
                "authorization_endpoint": metadata.get("authorization_endpoint"),
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Unable to connect to Microsoft Entra ID",
                    "error": str(e),
                }
            ),
            500,
        )


# Registers with Entra ID
@auth_bp.route("/auth/login", methods=["GET"])
def get_login_url():
    """Generates the login URL and caches the PKCE keys in the backend session."""
    msal_client = build_msal_app()

    # 1. Generate the flow context containing the crucial PKCE keys
    flow = msal_client.initiate_auth_code_flow(
        scopes=["User.read"],
        redirect_uri=current_app.config["ENTRA_AZURE_REDIRECT_URI"],
    )

    # 2. Store the flow data in the BACKEND session for verification later
    session["active_auth_flow"] = flow

    # 3. Return the URL to the caller
    return jsonify({"auth_uri": flow["auth_uri"]})


# with auth_code_flow
@auth_bp.route("/auth/exchange-code", methods=["POST"])
def exchange_code():
    """Validates the PKCE keys and exchanges the code using the active flow."""
    # 1. Retrieve the cached flow containing the verifier keys
    flow = session.pop("active_auth_flow", None)
    if not flow:
        return (
            jsonify(
                {
                    "error": "No matching authentication session found or session expired."
                }
            ),
            400,
        )

    data = request.get_json() or {}
    auth_response = data.get("auth_response") or {}

    # 2. Extract the code starting with '1.A...' from the payload
    code = auth_response.get("code")
    if not code:
        return jsonify({"error": "Missing authorization code"}), 400

    # 3. Reconstruct a clean response dictionary for MSAL to evaluate
    msal_auth_response = {
        "code": code,
        "state": flow.get("state"),  # Forces state matching to bypass manual state gaps
    }

    msal_client = build_msal_app()

    # 4. Exchange the code using the original flow context (PKCE keys are automatically handled here)
    result = msal_client.acquire_token_by_auth_code_flow(
        auth_code_flow=flow, auth_response=msal_auth_response
    )

    if "error" in result:
        return (
            jsonify(
                {
                    "error": result.get("error"),
                    "description": result.get("error_description"),
                }
            ),
            400,
        )

    return jsonify(
        {
            "user": result.get("id_token_claims"),
            "access_token": result.get("access_token"),
            "refresh_token": result.get("refresh_token"),
        }
    )


# After Entra ID, does a callback function
@auth_bp.route("/auth/callback/", methods=["GET"])
def entra_callback():

    if "error" in request.args:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": request.args.get("error_description")
                    or request.args.get("error"),
                }
            ),
            400,
        )

    if "code" not in request.args:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Authorization code not received.",
                }
            ),
            400,
        )

    code = request.args["code"]

    msal_app = build_msal_app()

    result = msal_app.acquire_token_by_authorization_code(
        code=code,
        scopes=[],
        redirect_uri=current_app.config["ENTRA_AZURE_REDIRECT_URI"],
    )

    if "error" in result:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": result.get("error_description") or result.get("error"),
                }
            ),
            401,
        )

    session["user"] = result.get("id_token_claims")
    session["access_token"] = result.get("access_token")

    return jsonify(
        {
            "status": "success",
            "message": "Successfully authenticated with Microsoft Entra ID.",
            "user": result.get("id_token_claims"),
        }
    )


# Register student
@auth_bp.route("/auth/register", methods=["POST"])
def register_student():
    response = request.get_json(silent=True)

    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )

    try:
        student_data = StudentCreate.model_validate(response)

    except ValidationError as e:
        print("============================")
        print("ERROR:", e)
        print("ERRORS: ", e.errors())
        print("JSON: ", e.json())
        print("============================")

        details = {}

        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "request"
            details[field] = error["msg"]

        return (
            jsonify(
                {
                    "error": "Bad request.",
                    "message": "Invalid request body.",
                    "details": details,
                }
            ),
            400,
        )
    # 2. Perform registration operation
    try:
        student = svc_register_student(student_data)
    except EmailAlreadyRegisteredError as e:
        return (
            jsonify(
                {
                    "error": "Conflict.",
                    "message": str(e),
                }
            ),
            409,
        )
    except IntegrityError:
        return (
            jsonify(
                {
                    "error": "Conflict.",
                    "message": "Registration conflicts with existing data.",
                }
            ),
            409,
        )
    except Exception as e:
        print("Registration failed:", e)

        return (
            jsonify(
                {
                    "error": "Internal server error.",
                    "message": "Student registration failed.",
                }
            ),
            500,
        )

    student_response = StudentResponse(
        student_id_bus=student.student_id_bus,
        first_name=student.first_name,
        last_name=student.last_name,
        mobile=student.mobile,
        dob=student.dob,
        role=student.user.role,
    )

    return jsonify(student_response.model_dump(mode="json")), 201


# Login student
@auth_bp.route("/login", methods=["POST"])
def login():
    response = request.get_json(silent=True)

    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )

    try:
        login_user = LoginRequest.model_validate(response)
    except ValidationError as e:
        details = {}

        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "request"
            details[field] = error["msg"]

        return (
            jsonify(
                {
                    "error": "Bad request.",
                    "message": "Invalid request body.",
                    "details": details,
                }
            ),
            400,
        )

    try:
        svc_login(login_user)
    except AuthenticationError as e:
        return (
            jsonify(
                {
                    "error": "Unauthorized.",
                    "message": str(e),
                }
            ),
            401,
        )
    return jsonify({"message": "Login successful"}), 200


# Register for SuperAdmins, Admins, Teachers
# SuperAd -> SuperAd, Admin, Teacher
# Admin -> Teacher
# Hence, to include Bearer Token
@auth_bp.route("/auth/staff", methods=["POST"])
def register_staff():
    response = request.get_json(silent=True)

    if not response:
        return (
            jsonify({"error": "Bad request.", "message": "Request body is required"}),
            400,
        )

    try:
        user_data = StaffCreate.model_validate(response)

    except ValidationError as e:
        pass

    staff = svc_register_staff(user_data)
    # print(f"User: {staff}")

    return (jsonify({"message": "auth user created"}), 201)
