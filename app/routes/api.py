from flask import Blueprint, jsonify, current_app
from ..services.roster import get_today_attendees

api_bp = Blueprint("api", __name__)

@api_bp.get("/attendances")
def api_attendances():
    names = get_today_attendees(current_app.config.get("MYSQL_URL"), current_app.config.get("APP_TIMEZONE"))
    return jsonify(names)
