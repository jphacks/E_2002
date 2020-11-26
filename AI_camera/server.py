import jphack
import json
from flask import Flask, jsonify
import subprocess
app = Flask(__name__)

@app.route('/api/start_yolo', methods=['GET'])
def start_yolo():
    state_file = open('state.json', 'r')
    state_json_file = json.load(state_file)
    state_json_file["state"] = "1"
    with open('state.json',"w") as f:
        json.dump(state_json_file,f, ensure_ascii=False)
    print(state_json_file)
    jphack.ready_yolo()
    return "0"

@app.route('/api/return_result', methods=['GET'])
def return_result():
    result_json = open('jphack.json',"r")
    json_return_result = json.load(result_json)
    print(json_return_result)
    print(jsonify(json_return_result))
    return jsonify(json_return_result)

@app.route('/api/overwrite_state', methods=['POST'])
def overwrite_state():
    context = {"state":"0"}
    with open('state.json',"w") as f:
        json.dump(context,f, ensure_ascii=False)
        
    return "0"

#sapp.run()


