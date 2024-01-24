from openai import OpenAI
import openai
import sys
import os
from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv
from src.utils.logandcatchexceptions import log_and_catch_exceptions
load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src'))
openai_api_key = os.getenv('DALLE3KEY')
openai.organization = os.getenv('OPENAI_ORGANIZATION')
openai.api_key = openai_api_key
dalle3_blueprint = Blueprint('dalle3', __name__)
@log_and_catch_exceptions
@dalle3_blueprint.route('/image', methods=['POST'])
def generate_image():
    openai_api_key = os.getenv('DALLE3KEY')
    client = OpenAI(api_key=openai_api_key)
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    return jsonify({"image_url": image_url})