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

limiter = Limiter(key_func=get_remote_address, default_limits=["30 per minute"])
limiter.init_app(app)

API_TOKEN = "SKIBIDI TOILET"

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        print(token)
        if not token or token != f"Bearer {API_TOKEN}":
            return jsonify({"error": "Unauthorized: Invalid or missing token"}), 401
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
@limiter.limit("30 per minute")
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
You are an AI debater.

Role: {role}  # 'attack' or 'defense'

Topic: {topic}

Opposing argument: {response}

Instructions:
- If your role is 'attack', argue AGAINST the topic.
- If your role is 'defense', argue FOR the topic.
- Defense must NEVER argue against the topic.
- Attack must NEVER argue for the topic.
- If you are unable to defend or attack the topic properly, respond with: "I give up you win."
- Keep answers short, clear, and focused.
- Your response should address points made by the opposing argument to engage in a meaningful debate.
- Feel free to ask questions or challenge the opposing side’s reasoning to encourage interaction.
- If you are starting the debate start with I support, or I oppose and state your argument.

Example:
Topic: We should imprison teens if they commit crimes.

Defense: "I support imprisoning teens because accountability is important and imprisonment can deter crime. However, how do you address the risk of harming teens' mental health through imprisonment?"

Attack: "I oppose imprisoning teens because it harms their development and there are better alternatives. But don’t you think lack of consequences might encourage repeat offenses?" 
"""
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": system_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4096
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return jsonify({"error": "Failed to get AI response", "details": response.text}), 500

    content = response.json()['choices'][0]['message']['content']
    return jsonify({"response": content})