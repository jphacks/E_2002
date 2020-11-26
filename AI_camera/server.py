import jphack
import json
from flask import Flask, jsonify
import subprocess
app = Flask(__name__)

#メインコンピュータからの命令によってAI Cameraを起動
@app.route('/api/start_yolo', methods=['GET'])
def start_yolo():
    #state.jsonを読み込みモードでオープン
    state_file = open('state.json', 'r')
    state_json_file = json.load(state_file)
    #"state"の値を0から1にする
    state_json_file["state"] = "1"
    #state.jsonを書き込みモードでオープン
    with open('state.json',"w") as f:
        #"state"の値を0から1に書き換える
        json.dump(state_json_file,f, ensure_ascii=False)
    print(state_json_file)
    
    #jphack.pyを実行してAI Cameraを起動
    jphack.ready_yolo()
    return "0"


#メインコンピュータに検出結果を求められたときに通達
@app.route('/api/return_result', methods=['GET'])
def return_result():
    #jphack.jsonを読み込みモードでオープン
    result_json = open('jphack.json',"r")
    #メインコンピュータに検出結果を通達
    json_return_result = json.load(result_json)
    print(json_return_result)
    print(jsonify(json_return_result))
    return jsonify(json_return_result)


#メインコンピュータからの命令によってAI Cameraを停止
@app.route('/api/overwrite_state', methods=['POST'])
def overwrite_state():
    #"state"の値を1から0にする
    context = {"state":"0"}
    #state.jsonを書き込みモードでオープン
    with open('state.json',"w") as f:
        #"state"の値を1から0に書き換える
        json.dump(context,f, ensure_ascii=False)
        
    return "0"

#sapp.run()


