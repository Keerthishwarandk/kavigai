from flask import Blueprint, request, jsonify
from app.controllers.controller import generate_web_link

web_link_bp = Blueprint('weblink', __name__)

@web_link_bp.route('/gen-web-links', methods=['POST'])
def generate():
    data = request.json
    goal = data.get('goal')
    if not goal:
        return jsonify({"error": "Goal is required"}), 400
    
    weblinks = generate_web_link(goal)
    return jsonify({"goal": goal, "roadmap": weblinks})
