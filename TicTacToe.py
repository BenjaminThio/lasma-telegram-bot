from telegram import InlineKeyboardButton, InlineKeyboardMarkup as Markup
from Handler import Edit
import json

Bot = "❌"
Player = "⭕️"
Turn = [Bot, Player]
Empty = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

def TicTacToe(update, context):
	with open("JSON/TicTacToe.json", "r") as jfile: jdata = json.load(jfile)
	UserID = update.effective_user.id
	if f"{UserID}_TicTacToe" not in jdata: jdata[f"{UserID}_TicTacToe"] = {"Board": dict(enumerate(Empty, start=1)), "Player": 1, "Moves": 0}
	with open("JSON/TicTacToe.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	Keyboard = [[]]
	Count = 0
	for i in jdata[f"{UserID}_TicTacToe"]["Board"]:
		Count += 1
		Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton(jdata[f"{UserID}_TicTacToe"]["Board"][i], callback_data=f"TicTacToe,{UserID},{i}"))
		if Count == 3: 
			Keyboard.append([]) 
			Count = 0
	update.effective_message.reply_text("Tic Tac Toe", reply_markup=Markup(Keyboard))

def TicTacToeQuery(Query):
	with open("JSON/TicTacToe.json", "r") as jfile: jdata = json.load(jfile)
	UserID = Query.data.split(",")[1]
	Pressed = Query.data.split(",")[2]
	if f"{UserID}_TicTacToe" not in jdata: return Edit(Query, "This game has ended!")
	def Update(Text, GameOver):
		Keyboard = [[]]
		Count = 0
		for i in jdata[f"{UserID}_TicTacToe"]["Board"]:
			Count += 1
			if not GameOver: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton(jdata[f"{UserID}_TicTacToe"]["Board"][i], callback_data=f"TicTacToe,{UserID},{i}"))
			else: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton(jdata[f"{UserID}_TicTacToe"]["Board"][i], callback_data="None"))
			if Count == 3: 
				Keyboard.append([])
				Count = 0
		try: Edit(Query, Text, Markup(Keyboard))
		except Exception as Error: Query.bot.answer_callback_query(callback_query_id=Query.id, text=Error, show_alert=True)
	def Check(Player):
		Board = jdata[f"{UserID}_TicTacToe"]["Board"]
		if Board["1"] == Board["2"] == Board["3"]: return True
		elif Board["4"] == Board["5"] == Board["6"]: return True
		elif Board["7"] == Board["8"] == Board["9"]: return True
		elif Board["1"] == Board["4"] == Board["7"]: return True
		elif Board["2"] == Board["5"] == Board["8"]: return True
		elif Board["3"] == Board["6"] == Board["9"]: return True
		elif Board["1"] == Board["5"] == Board["9"]: return True
		elif Board["3"] == Board["5"] == Board["7"]: return True
		return False
	if jdata[f"{UserID}_TicTacToe"]["Board"][Pressed] not in Turn:
		jdata[f"{UserID}_TicTacToe"]["Board"][Pressed] = Turn[jdata[f"{UserID}_TicTacToe"]["Player"] - 1]
		jdata[f"{UserID}_TicTacToe"]["Moves"] += 1
		with open("JSON/TicTacToe.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
		if Check(Turn[jdata[f"{UserID}_TicTacToe"]["Player"] - 1]):
			Update("Player " + str(jdata[f"{UserID}_TicTacToe"]["Player"]) + " won!", True)
			del jdata[f"{UserID}_TicTacToe"]
			with open("JSON/TicTacToe.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
			return
		elif jdata[f"{UserID}_TicTacToe"]["Moves"] == 9:
			Update("Draw!", True)
			del jdata[f"{UserID}_TicTacToe"]
			with open("JSON/TicTacToe.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
			return
		if jdata[f"{UserID}_TicTacToe"]["Player"] == 1: jdata[f"{UserID}_TicTacToe"]["Player"] = 2
		else: jdata[f"{UserID}_TicTacToe"]["Player"] = 1
		with open("JSON/TicTacToe.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
		Update("Tic Tac Toe", False)
	else: Query.bot.answer_callback_query(callback_query_id=Query.id, text="Please choose a different place!")

def UpdateAI(UserID, GameOver):
	with open("JSON/TicTacToeAI.json", "r") as jfile: jdata = json.load(jfile)
	j = jdata[f"{UserID}_TicTacToeAI"]
	Count = 0
	Keyboard = [[]]
	for i in j:
		Count += 1
		if not GameOver: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton(j[i], callback_data=f"TicTacToeAI,{UserID},{i}"))
		else: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton(j[i], callback_data="None"))
		if Count == 3:
			Count = 0
			Keyboard.append([])
	return Markup(Keyboard)

def TicTacToeAI(update, context):
	with open("JSON/TicTacToeAI.json", "r") as jfile: jdata = json.load(jfile)
	UserID = update.effective_user.id
	if UserID not in jdata: jdata[f"{UserID}_TicTacToeAI"] = dict(enumerate(Empty, start=1))
	with open("JSON/TicTacToeAI.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	update.effective_message.reply_text("Tic Tac Toe AI", reply_markup=UpdateAI(UserID, False))

def TicTacToeAIQuery(Query):
	with open("JSON/TicTacToeAI.json", "r") as jfile: jdata = json.load(jfile)
	Data = Query.data.split(",")
	UserID = Data[1]
	j = jdata[f"{UserID}_TicTacToeAI"]
	def Free(Position):
		if j[Position] in Empty: return True
		else: return False
	def Draw():
		for key in j.keys():
			if (j[key] in Empty): return False
		return True
	def CheckWin():
		if (j["1"] == j["2"] == j["3"]): return True
		elif (j["4"] == j["5"] == j["6"]): return True
		elif (j["7"] == j["8"] == j["9"]): return True
		elif (j["1"] == j["4"] == j["7"]): return True
		elif (j["2"] == j["5"] == j["8"]): return True
		elif (j["3"] == j["6"] == j["9"]): return True
		elif (j["1"] == j["5"] == j["9"]): return True
		elif (j["7"] == j["5"] == j["3"]): return True
		else: return False
	def Check(Mark):
		if j["1"] == j["2"] == j["3"] == Mark: return True
		elif (j["4"] == j["5"] == j["6"] == Mark): return True
		elif (j["7"] == j["8"] == j["9"] == Mark): return True
		elif (j["1"] == j["4"] == j["7"] == Mark): return True
		elif (j["2"] == j["5"] == j["8"] == Mark): return True
		elif (j["3"] == j["6"] == j["9"] == Mark): return True
		elif (j["1"] == j["5"] == j["9"] == Mark): return True
		elif (j["3"] == j["5"] == j["7"] == Mark): return True
		else: return False
	def Insert(Letter, Position):
		if int(Position) > 0 and Free(Position):
			j[Position] = Letter
			with open("JSON/TicTacToeAI.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
			Query.edit_message_text("Tic Tac Toe AI", reply_markup=UpdateAI(UserID, False))
			if (Draw()):
				Query.edit_message_text("Draw!", reply_markup=UpdateAI(UserID, True))
				del jdata[f"{UserID}_TicTacToeAI"]
			if CheckWin():
				if Letter == Bot: Query.edit_message_text("Bot won!", reply_markup=UpdateAI(UserID, True))
				else: Query.edit_message_text("Player won!", reply_markup=UpdateAI(UserID, True))
				del jdata[f"{UserID}_TicTacToeAI"]
			with open("JSON/TicTacToeAI.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	def Minimax(j, Depth, Maximizing):
		if (Check(Bot)): return 1
		elif (Check(Player)): return -1
		elif (Draw()): return 0
		if (Maximizing):
			BestScore = -1
			for key in j.keys():
				if (j[key] in Empty):
					j[key] = Bot
					Score = Minimax(j, Depth + 1, False)
					j[key] = Empty[int(key) - 1]
					if (Score > BestScore): BestScore = Score
			return BestScore
		else:
			BestScore = 1
			for key in j.keys():
				if (j[key] in Empty):
					j[key] = Player
					Score = Minimax(j, Depth + 1, True)
					j[key] = Empty[int(key) - 1]
					if (Score < BestScore): BestScore = Score
			return BestScore
	if j[Data[-1]] in Empty: Insert(Player, Data[-1])
	else: return
	BestScore = -1
	BestMove = 0
	for key in j.keys():
		if (j[key] in Empty):
			j[key] = Bot
			score = Minimax(j, 0, False)
			j[key] = Empty[int(key) - 1]
			if (score > BestScore):
				BestScore = score
				BestMove = key
	Insert(Bot, BestMove)