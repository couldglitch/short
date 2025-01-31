from flask import Flask, jsonify, redirect, render_template, request
import requests

app = Flask(__name__)

# URL of the Google Apps Script that returns JSON data
DATA_URL = "https://script.google.com/macros/s/AKfycbxqw6PD2GW4ektUCs36ZMPKYhECKuVdh76YBczDIZ4S8oqWluSMJBR0266jblHUJG37Rg/exec"

def load_data():
    response = requests.get(DATA_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    data = load_data()
    return jsonify(data)

@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    data = load_data()
    # Find the original URL based on the short_url
    for item in data:
        if item['short_url'] == short_url:
            return redirect(item['original_url'], code=302)
    return jsonify({"error": "Short URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)