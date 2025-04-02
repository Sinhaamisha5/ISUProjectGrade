from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS
#from import CORS
import ghana
import china
import nigeria
import india

app = Flask(__name__)
CORS(app)




@app.route('/get_grade_point', methods=['GET'])
def get_grade_point():
    return ghana.get_grade_point()


@app.route('/get_China_grade_point', methods=['GET'])
def get_grade_point_china():
    return china.get_grade_point_china()

@app.route('/get_Nigeria_grade_point', methods=['GET'])  
def get_grade_point_nigeria():
    return nigeria.get_grade_point_nigeria()

@app.route('/get_India_grade_point', methods=['GET'])  
def get_grade_point_india():
    return india.get_grade_point_india()



if __name__ == '__main__':
    print("Starting Flask server...")  # Debugging output
    app.run(debug=True, host='0.0.0.0', port=5000)
