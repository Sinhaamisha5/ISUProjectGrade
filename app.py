from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS
#from import CORS
import ghana
import china
import nigeria
import india
from flask import send_file

app = Flask(__name__)
CORS(app)

@app.route('/get_grade_point', methods=['GET'])
def get_grade_point():
    return ghana.get_grade_point()

@app.route('/get_ghana_universities', methods=['GET'])
def get_ghana_universities():
    return ghana.get_ghana_universities()


@app.route('/get_China_grade_point', methods=['GET'])
def get_grade_point_china():
    return china.get_grade_point_china()

@app.route('/get_china_universities', methods=['GET'])
def get_china_universities():
    return china.get_china_universities()

@app.route('/get_Nigeria_grade_point', methods=['GET'])  
def get_grade_point_nigeria():
    return nigeria.get_grade_point_nigeria()

@app.route('/get_nigeria_universities', methods=['GET'])
def get_nigeria_universities():
    return nigeria.get_nigeria_universities()

@app.route('/get_India_grade_point', methods=['GET'])  
def get_grade_point_india():
    return india.get_grade_point_india()  

@app.route('/get_india_universities', methods=['GET'])
def get_india_universities():
    return india.get_india_universities()


#download link
@app.route('/download/ghana', methods=['GET'])
def download_ghana_file():
    file_path = "Ghana List.xlsx"
    return send_file(file_path, as_attachment=True)

@app.route('/download/nigeria', methods=['GET'])
def download_nigeria_file():
    file_path = "Nigeria List.xlsx"
    return send_file(file_path, as_attachment=True)

@app.route('/download/china', methods=['GET'])
def download_china_file():
    file_path = "China List.xlsx"  # or whatever you're using for China
    return send_file(file_path, as_attachment=True)

@app.route('/download/india', methods=['GET'])
def download_india_file():
    file_path = "India List.xlsx"  # same file used for India
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    print("Starting Flask server...")  # Debugging output
    app.run(debug=True, host='0.0.0.0', port=5000)
