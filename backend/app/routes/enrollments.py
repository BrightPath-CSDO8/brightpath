from flask import Blueprint, request, jsonify
from pydantic import ValidationError

enrollment_bp = Blueprint("enrollment", __name__)


@enrollment_bp.route("/api/v1/enrollments", methods=["POST"])
def enrollments():
    response = request.get_json(silent=True)
