from flask import Flask, jsonify, request
from markovify import NewlineText
import requests as req
import os, sys

# Setup CORS
from flask_cors import CORS

# Setup environmental values
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)

# Set environmental values
if 'ENDPOINT' in os.environ and 'SUBSCRIPTION_KEY' in os.environ:
    endpoint = os.environ['ENDPOINT']
    subscription_key = os.environ['SUBSCRIPTION_KEY']

# Test url
@app.route('/', methods=['GET'])
def test():
    return 'test'

# Post url
@app.route('/api/generate', methods=['POST'])
def analyze_image():
    # Get image data from body
    file = request.files['file']

    # Post header
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    # Post params
    params = {
        'visualFeatures': 'Description',
        'language': 'ja'
    }

    # Call API and get tags
    try:
        res = req.post(endpoint, headers=headers, params=params, data=file)
        tags = res.json()['description']['tags']
    except Exception as e:
        print(e)

    splited_text = open('./resources/splited.txt').read()
    text_model = NewlineText(splited_text)

    for tag in tags:
        try:
            sentence = text_model.make_sentence_with_start(tag, tries=300, max_overlap_ratio=0.7).replace(' ', '')
            return sentence
        except:
            pass
    return text_model.make_sentence(tries=300, max_overlap_ratio=0.7).replace(' ', '')

# Error handling
@app.errorhandler(Exception)
def error_handler(e):
    code = 500
    return jsonify({
        'error': str(e)
    }), code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'], debug=True)