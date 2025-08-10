import os
import requests
from flask import Flask, Blueprint, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from AIClashArena import app
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

api_bp = Blueprint('API', __name__)

limiter = Limiter(app, key_func=get_remote_address, default_limits=["5 per minute"])

API_TOKEN = "SKIBIDI TOILET"

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or token != f"Bearer {API_TOKEN}":
            abort(401, description="Unauthorized: Invalid or missing token")
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

@api_bp.route("/get_ai_response", methods=["POST"])
@token_required
@limiter.limit("3 per minute")
def get_ai_response():
    data = request.get_json()
    topic = data.get("topic")
    if not topic:
        return jsonify({"error": "Missing 'topic' in request"}), 400
    
    role = data.get("role")
    if not role:
        return jsonify({"error": "Missing 'role' in request"}), 400
    
    response = data.get("response")
    
    system_prompt = f"""
    You are an AI designed to engage in thoughtful and balanced debates. Your task is to analyze the given topic from your assigned role, consider the opposing viewpoint, and respond with clear, logical, and well-reasoned arguments.  
    Your role is {role}. If the previous response is empty, initiate the debate accordingly."""
    
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": response},
            {"role": "user", "content": topic}
        ],
        "temperature": 0.7,
        "max_tokens": 4096
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return jsonify({"error": "Failed to get AI response", "details": response.text}), 500

    content = response.json()['choices'][0]['message']['content']
    return jsonify({"response": content})