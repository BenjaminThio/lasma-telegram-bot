from flask import Flask, jsonify, request
from threading import Thread
from Datetime import Datetime
import json
import uuid

Limitation = [3, 20]

def Lasma(update, context): pass

def LasmaQuery(update, context): pass

def LasmaText(update, context): pass

app = Flask(__name__)

@app.route("/")
def home(): return "╔╗───────────────╔═══╗╔╗─────╔╗\n║║───────────────║╔═╗╠╝╚╗────║║\n║║──╔══╦══╦╗╔╦══╗║╚══╬╗╔╬╗╔╦═╝╠╦══╗\n║║─╔╣╔╗║══╣╚╝║╔╗║╚══╗║║║║║║║╔╗╠╣╔╗║\n║╚═╝║╔╗╠══║║║║╔╗║║╚═╝║║╚╣╚╝║╚╝║║╚╝║\n╚═══╩╝╚╩══╩╩╩╩╝╚╝╚═══╝╚═╩══╩══╩╩══╝"

@app.route("/add-leaderboard")
def AddLeaderboard():
	with open("JSON/Leaderboard.json", "r") as jfile: jdata = json.load(jfile)
	Token = uuid.uuid4()
	while f"{Token}_Leaderboard" in jdata: Token = uuid.uuid4()
	jdata[f"{Token}_Leaderboard"] = {"Name": None, "PlayerData": {}}
	with open("JSON/Leaderboard.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	return jsonify({"Message": "A new leaderboard has been created!", "Token": Token}), 200

@app.route("/delete-leaderboard")
def DeleteLeaderboard():
	Token = request.args.get("token", type = str)
	with open("JSON/Leaderboard.json", "r") as jfile: jdata = json.load(jfile)
	if f"{Token}_Leaderboard" in jdata: del jdata[f"{Token}_Leaderboard"]
	else: return jsonify({"Message": "Token not found!"}), 404
	with open("JSON/Leaderboard.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	return jsonify({"Message": f"{Token} has been deleted!"}), 200

@app.route("/add-player")
def AddPlayer():
	Token = request.args.get("token", type = str)
	Name = request.args.get("name", type = str)
	Score = request.args.get("score", default = 0, type = int)
	with open("JSON/Leaderboard.json", "r") as jfile: jdata = json.load(jfile)
	ID = str(uuid.uuid4())[:8]
	while ID in jdata[f"{Token}_Leaderboard"]["PlayerData"]: ID = str(uuid.uuid4())[:8]
	if f"{Token}_Leaderboard" in jdata:
		if len(Name.strip()) <= Limitation[1]: jdata[f"{Token}_Leaderboard"]["PlayerData"][ID] = {"Name": Name, "Score": Score, "Date": Datetime("Asia/Kuala_Lumpur", "%d/%m/%Y"), "Time": Datetime("Asia/Kuala_Lumpur", "%I:%M%p")}
		else: jsonify({"Message": f"The name given should be less than {Limitation[1]} letters!"}), 411
	else: return jsonify({"Message": "Token not found!"}), 404
	jdata[f"{Token}_Leaderboard"]["PlayerData"] = {i:jdata[f"{Token}_Leaderboard"]["PlayerData"][i] for i in [i[0] for i in sorted(jdata[f"{Token}_Leaderboard"]["PlayerData"].items(), key=lambda x: x[1]["Score"], reverse=True)]}
	with open("JSON/Leaderboard.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	return jsonify({"Message": f"{Name} has been added!", "ID": ID}), 201

@app.route("/delete-player")
def DeletePlayer():
	Token = request.args.get("token", type = str)
	ID = request.args.get("id", type = str)
	with open("JSON/Leaderboard.json", "r") as jfile: jdata = json.load(jfile)
	if f"{Token}_Leaderboard" in jdata:
		if ID in jdata[f"{Token}_Leaderboard"]["PlayerData"]:
			Name = jdata[f"{Token}_Leaderboard"]["PlayerData"][ID]["Name"]
			del jdata[f"{Token}_Leaderboard"]["PlayerData"][ID]
		else: jsonify({"Message": "ID not found!"}), 404
	else: return jsonify({"Message": "Token not found!"}), 404
	with open("JSON/Leaderboard.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	return jsonify({"Message": f"{Name} has been deleted!"}), 200

@app.route("/update-player-score")
def UpdatePlayerScore():
	Token = request.args.get("token", type = str)
	ID = request.args.get("id", type = str)
	Score = request.args.get("score", type = int)
	with open("JSON/Leaderboard.json", "r") as jfile: jdata = json.load(jfile)
	if f"{Token}_Leaderboard" in jdata:
		if ID in jdata[f"{Token}_Leaderboard"]["PlayerData"]:
			jdata[f"{Token}_Leaderboard"]["PlayerData"][ID]["Score"] = Score
			jdata[f"{Token}_Leaderboard"]["PlayerData"][ID]["Date"] = Datetime("Asia/Kuala_Lumpur", "%d/%m/%Y")
			jdata[f"{Token}_Leaderboard"]["PlayerData"][ID]["Time"] = Datetime("Asia/Kuala_Lumpur", "%I:%M%p")
		else: return jsonify({"Message": "ID not found!"}), 404
	else: return jsonify({"Message": "Token not found!"}), 404
	jdata[f"{Token}_Leaderboard"]["PlayerData"] = {i:jdata[f"{Token}_Leaderboard"]["PlayerData"][i] for i in [i[0] for i in sorted(jdata[f"{Token}_Leaderboard"]["PlayerData"].items(), key=lambda x: x[1]["Score"], reverse=True)]}
	with open("JSON/Leaderboard.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	return jsonify({"Message": "{}'s score has been updated to {}!".format(jdata[f"{Token}_Leaderboard"]["PlayerData"][ID]["Name"], jdata[f"{Token}_Leaderboard"]["PlayerData"][ID]["Score"])}), 200

@app.route("/get-player-data")
def GetPlayerData():
	Token = request.args.get("token", type = str)
	ID = request.args.get("id", type = str)
	with open("JSON/Leaderboard.json", "r") as jfile: jdata = json.load(jfile)
	if f"{Token}_Leaderboard" in jdata:
		if ID in jdata[f"{Token}_Leaderboard"]["PlayerData"]: return jsonify(jdata[f"{Token}_Leaderboard"]["PlayerData"][ID]), 200
		else: return jsonify({"Message": "ID not found!"}), 404
	else: return jsonify({"Message": "Token not found!"}), 404

@app.route("/get-all-player-data")
def GetAllPlayerData():
	Token = request.args.get("token", type = str)
	with open("JSON/Leaderboard.json", "r") as jfile: jdata = json.load(jfile)
	if f"{Token}_Leaderboard" in jdata: return jsonify(jdata[f"{Token}_Leaderboard"]["PlayerData"]), 200
	else: return jsonify({"Message": "Token not found!"}), 404

def Run(): app.run(host="0.0.0.0", port=0000)

def Alive(): Thread(target=Run).start()