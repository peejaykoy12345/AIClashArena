import os
import requests
from flask import Flask, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from AIClashArena import app
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

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

@token_required
def get_ai_response():
    system_prompt = ""
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input}
        ],
        "temperature": 0.7,
        "max_tokens": 4096
    }
    response = requests.post(url, headers=headers, json=data)