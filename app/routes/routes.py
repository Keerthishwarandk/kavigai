from flask import Blueprint, request, jsonify
from app.controllers.controller import google_custom_search , get_goal_template

web_link_bp = Blueprint('weblink', __name__)

@web_link_bp.route('/gen-web-links', methods=['POST'])
def generate():
    data = request.json
    goal = data.get('goal')
    if not goal:
        return jsonify({"error": "Goal is required"}), 400
    
    API_KEY = "AIzaSyB4_2NLQApl_UA7RhClX_j5AT-5OY1uSts"
    CSE_ID = "b4ef5beef8dc14fed"
    weblinks = google_custom_search(API_KEY, CSE_ID, goal)
    return jsonify({"goal": goal, "roadmap": weblinks})


@web_link_bp.route('/gen-goal-template', methods=['POST'])
def generate_goal_template():
    data = request.json
    goal = data.get('goaltemp')
    fromdate = data.get('fromdate')
    todate = data.get('todate')
    if not goal:
        return jsonify({"error": "Goal is required"}), 400
    
   
    templates = get_goal_template(goal,fromdate,todate)
    return jsonify({"goal": goal, "roadmap": templates})
