from flask import Flask, jsonify
from multicrawler import get_json, get_csv

app = Flask(__name__)

@app.route('/json', methods=['GET'])
def get_scrapy_json():
	return jsonify(get_json())

@app.route('/csv', methods=['GET'])
def get_scrapy_csv():
	return jsonify(get_csv())

app.run(port=5000)