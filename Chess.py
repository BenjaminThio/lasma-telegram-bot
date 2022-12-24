from telegram import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
from telegram import InputMediaPhoto
from PIL import Image, ImageDraw, ImageFont
import json
import os

Width = 8
Height = 8
Pieces = {0: ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"], 1: ["♟"] * Width, 6: ["♙"] * Width, 7: ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]}
Player = {True: ["♙", "♖", "♘", "♗", "♕", "♔"], False: ["♟", "♜", "♞", "♝", "♛", "♚"]}
Score = {"♙": 1, "♟": 1, "♘": 3, "♞": 3, "♗": 3, "♝": 3, "♖": 5, "♜": 5, "♕": 9, "♛": 9}

def GenerateChess():
	Chess = []
	for y in range(Height):
		for x in range(Width):
			if (y + x) % 2 == 1: Chess.append("⬛️")
			else: Chess.append("⬜️")
	return [Chess[i: i + Width] for i in range(0, len(Chess), Height)]

def UpdateChess(UserID, GameOver=None):
	with open("JSON/Chess.json", "r") as jfile: jdata = json.load(jfile)
	Keyboard = []
	IMG = Image.new("RGB", (Width * 60, (Height + 1) * 60), color="White")
	for y in range(len(jdata[f"{UserID}_Chess"]["Board"])):
		for x in range(len(jdata[f"{UserID}_Chess"]["Board"][y])):
			if (x + y) % 2 == 1: ImageDraw.Draw(IMG).rectangle([(x * 60, y * 60), ((x * 60) + 60, (y * 60) + 60)], fill="Grey")
			if [x, y] == jdata[f"{UserID}_Chess"]["Selected"]: ImageDraw.Draw(IMG).rectangle([(x * 60, y * 60), ((x * 60) + 60, (y * 60) + 60)], fill="Red", outline="Black")
			if [x, y] in jdata[f"{UserID}_Chess"]["Valid"]: ImageDraw.Draw(IMG).rectangle([(x * 60, y * 60), ((x * 60) + 60, (y * 60) + 60)], fill="Green", outline="Black")
			if [x, y] == GameOver: IMG.paste(Image.open("Chess/Galaxy.png"), (x * 60, y * 60))
			if jdata[f"{UserID}_Chess"]["Board"][y][x] not in ["⬜️", "⬛️"]: IMG.paste(Image.open("Chess/" + jdata[f"{UserID}_Chess"]["Board"][y][x] + ".png"), (x * 60, y * 60), mask=Image.open("Chess/" + jdata[f"{UserID}_Chess"]["Board"][y][x] + ".png"))
			Keyboard.append(Button(jdata[f"{UserID}_Chess"]["Board"][y][x], callback_data=f"Chess,{UserID},{x}:{y}"))
	if GameOver != None: ImageDraw.Draw(IMG).text((0, Height * 60), "{} has won the game with score: {}".format(["Black", "White"][int(jdata[f"{UserID}_Chess"]["Player"])], jdata[f"{UserID}_Chess"]["Score"][int(jdata[f"{UserID}_Chess"]["Player"])]), font=ImageFont.truetype("Chess/Roboto.ttf", 25), fill="Black")
	else: ImageDraw.Draw(IMG).text((0, Height * 60), "Current Turn: {}\nBlack's Score: {}\nWhite's Score: {}".format({0: "Black", 1: "White"}[int(jdata[f"{UserID}_Chess"]["Player"])], jdata[f"{UserID}_Chess"]["Score"][0], jdata[f"{UserID}_Chess"]["Score"][1]), font=ImageFont.truetype("Chess/Roboto.ttf", 18), fill="Black")
	IMG.save("Clients/Chess.png")
	return Markup([Keyboard[i: i + Width] for i in range(0, len(Keyboard), Height)])

def Chess(update, context):
	with open("JSON/Chess.json", "r") as jfile: jdata = json.load(jfile)
	UserID = update.effective_user.id
	Chess = GenerateChess()
	for i in Pieces: Chess[i] = Pieces[i]
	if f"{UserID}_Chess" not in jdata: jdata[f"{UserID}_Chess"] = {"Board": Chess, "Selected": None,"Valid": [], "Player": True, "Score": [0, 0]}
	with open("JSON/Chess.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	context.bot.send_photo(chat_id=update.effective_message.chat_id, reply_markup=UpdateChess(UserID), photo=open("Clients/Chess.png", "rb"))
	os.remove("Clients/Chess.png")

def ChessQuery(Query):
	with open("JSON/Chess.json", "r") as jfile: jdata = json.load(jfile)
	Data = Query.data.split(",")
	UserID = Data[1]
	Coord = [int(i) for i in Data[-1].split(":")]
	if jdata[f"{UserID}_Chess"]["Selected"] == None and jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in Player[jdata[f"{UserID}_Chess"]["Player"]] or jdata[f"{UserID}_Chess"]["Selected"] != [Coord[0], Coord[1]] and jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in Player[jdata[f"{UserID}_Chess"]["Player"]]:
		if jdata[f"{UserID}_Chess"]["Selected"] != [Coord[0], Coord[1]] and jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in Player[jdata[f"{UserID}_Chess"]["Player"]]: jdata[f"{UserID}_Chess"]["Valid"] = []
		if jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in Player[not jdata[f"{UserID}_Chess"]["Player"]]: return Query.bot.answer_callback_query(callback_query_id=Query.id, text="Not your turn!")
		jdata[f"{UserID}_Chess"]["Selected"] = [Coord[0], Coord[1]]
		if jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♙", "♟"]:
			if jdata[f"{UserID}_Chess"]["Board"][Coord[1] + 1 * {"♙": -1, "♟": 1}[jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]]]][Coord[0]] in ["⬜️", "⬛️"]: jdata[f"{UserID}_Chess"]["Valid"].append([Coord[0], Coord[1] + 1 * {"♙": -1, "♟": 1}[jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]]]])
			if Coord[1] == {"♙": 6, "♟": 1}[jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]]] and jdata[f"{UserID}_Chess"]["Board"][Coord[1] + 1 * {"♙": -1, "♟": 1}[jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]]]][Coord[0]] in ["⬜️", "⬛️"] and jdata[f"{UserID}_Chess"]["Board"][Coord[1] + 2 * {"♙": -1, "♟": 1}[jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]]]][Coord[0]] in ["⬜️", "⬛️"]: jdata[f"{UserID}_Chess"]["Valid"].append([Coord[0], Coord[1] + 2 * {"♙": -1, "♟": 1}[jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]]]])
			for i in [1, -1]:
				if Coord[0] + i >= 0 and Coord[0] + i < Width:
					if jdata[f"{UserID}_Chess"]["Board"][Coord[1] + 1 * {"♙": -1, "♟": 1}[jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]]]][Coord[0] + i] in Player[not jdata[f"{UserID}_Chess"]["Player"]]: jdata[f"{UserID}_Chess"]["Valid"].append([Coord[0] + i, Coord[1] + 1 * {"♙": -1, "♟": 1}[jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]]]])
				else: continue
		if jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♘", "♞"]:
			for i in [[Coord[0] - 1, Coord[1] + 2], [Coord[0] - 2, Coord[1] + 1], [Coord[0] + 1, Coord[1] + 2], [Coord[0] + 2, Coord[1] + 1], [Coord[0] - 1, Coord[1] - 2], [Coord[0] - 2, Coord[1] - 1], [Coord[0] + 1, Coord[1] - 2], [Coord[0] + 2, Coord[1] - 1]]:
				if i[0] < Width and i[1] < Height:
					if jdata[f"{UserID}_Chess"]["Board"][i[1]][i[0]] not in Player[jdata[f"{UserID}_Chess"]["Player"]]: jdata[f"{UserID}_Chess"]["Valid"].append([i[0], i[1]])
		if jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♖", "♜", "♕", "♛", "♔", "♚"]:
			for i in range(1, Width):
				if Coord[0] + i < Width and jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0] + i] not in Player[jdata[f"{UserID}_Chess"]["Player"]]:
					jdata[f"{UserID}_Chess"]["Valid"].append([Coord[0] + i, Coord[1]])
					if jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0] + i] in Player[not jdata[f"{UserID}_Chess"]["Player"]] or jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♔", "♚"]: break
				else: break
			for i in range(1, Width):
				if Coord[0] - i >= 0 and jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0] - i] not in Player[jdata[f"{UserID}_Chess"]["Player"]]:
					jdata[f"{UserID}_Chess"]["Valid"].append([Coord[0] - i, Coord[1]])
					if jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0] - i] in Player[not jdata[f"{UserID}_Chess"]["Player"]] or jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♔", "♚"]: break
				else: break
			for i in range(1, Height):
				if Coord[1] + i < Height and jdata[f"{UserID}_Chess"]["Board"][Coord[1] + i][Coord[0]] not in Player[jdata[f"{UserID}_Chess"]["Player"]]:
					jdata[f"{UserID}_Chess"]["Valid"].append([Coord[0], Coord[1] + i])
					if jdata[f"{UserID}_Chess"]["Board"][Coord[1] + i][Coord[0]] in Player[not jdata[f"{UserID}_Chess"]["Player"]] or jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♔", "♚"]: break
				else: break
			for i in range(1, Height):
				if Coord[1] - i >= 0 and jdata[f"{UserID}_Chess"]["Board"][Coord[1] - i][Coord[0]] not in Player[jdata[f"{UserID}_Chess"]["Player"]]:
					jdata[f"{UserID}_Chess"]["Valid"].append([Coord[0], Coord[1] - i])
					if jdata[f"{UserID}_Chess"]["Board"][Coord[1] - i][Coord[0]] in Player[not jdata[f"{UserID}_Chess"]["Player"]] or jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♔", "♚"]: break
				else: break
		if jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♗", "♝", "♕", "♛", "♔", "♚"]:
			for i in range(1, Width):
				if Coord[0] + i < Width and Coord[1] - i >= 0 and jdata[f"{UserID}_Chess"]["Board"][Coord[1] - i][Coord[0] + i] not in Player[jdata[f"{UserID}_Chess"]["Player"]]:
					jdata[f"{UserID}_Chess"]["Valid"].append([Coord[0] + i, Coord[1] - i])
					if jdata[f"{UserID}_Chess"]["Board"][Coord[1] - i][Coord[0] + i] in Player[not jdata[f"{UserID}_Chess"]["Player"]] or jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♔", "♚"]: break
				else: break
			for i in range(1, Width):
				if Coord[0] - i >= 0 and Coord[1] - i >= 0 and jdata[f"{UserID}_Chess"]["Board"][Coord[1] - i][Coord[0] - i] not in Player[jdata[f"{UserID}_Chess"]["Player"]]:
					jdata[f"{UserID}_Chess"]["Valid"].append([Coord[0] - i, Coord[1] - i])
					if jdata[f"{UserID}_Chess"]["Board"][Coord[1] - i][Coord[0] - i] in Player[not jdata[f"{UserID}_Chess"]["Player"]] or jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♔", "♚"]: break
				else: break
			for i in range(1, Height):
				if Coord[0] + i < Width and Coord[1] + i < Height and jdata[f"{UserID}_Chess"]["Board"][Coord[1] + i][Coord[0] + i] not in Player[jdata[f"{UserID}_Chess"]["Player"]]:
					jdata[f"{UserID}_Chess"]["Valid"].append([Coord[0] + i, Coord[1] + i])
					if jdata[f"{UserID}_Chess"]["Board"][Coord[1] + i][Coord[0] + i] in Player[not jdata[f"{UserID}_Chess"]["Player"]] or jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♔", "♚"]: break
				else: break
			for i in range(1, Height):
				if Coord[0] - i < Width and Coord[1] + i < Height and jdata[f"{UserID}_Chess"]["Board"][Coord[1] + i][Coord[0] - i] not in Player[jdata[f"{UserID}_Chess"]["Player"]]:
					jdata[f"{UserID}_Chess"]["Valid"].append([Coord[0] - i, Coord[1] + i])
					if jdata[f"{UserID}_Chess"]["Board"][Coord[1] + i][Coord[0] - i] in Player[not jdata[f"{UserID}_Chess"]["Player"]] or jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] in ["♔", "♚"]: break
				else: break
	elif jdata[f"{UserID}_Chess"]["Selected"] != [Coord[0], Coord[1]] and [Coord[0], Coord[1]] in jdata[f"{UserID}_Chess"]["Valid"] or jdata[f"{UserID}_Chess"]["Selected"] == [Coord[0], Coord[1]]:
		if jdata[f"{UserID}_Chess"]["Selected"] != [Coord[0], Coord[1]]:
			if jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] not in ["⬜️", "⬛️", "♔", "♚"]: jdata[f"{UserID}_Chess"]["Score"][int(jdata[f"{UserID}_Chess"]["Player"])] += Score[jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]]]
			jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] = jdata[f"{UserID}_Chess"]["Board"][jdata[f"{UserID}_Chess"]["Selected"][1]][jdata[f"{UserID}_Chess"]["Selected"][0]]
			if jdata[f"{UserID}_Chess"]["Board"][jdata[f"{UserID}_Chess"]["Selected"][1]][jdata[f"{UserID}_Chess"]["Selected"][0]] in ["♙", "♟"] and Coord[1] in [0, Height - 1]: jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] = {0: "♕", Height - 1: "♛"}[Coord[1]]
			jdata[f"{UserID}_Chess"]["Board"][jdata[f"{UserID}_Chess"]["Selected"][1]][jdata[f"{UserID}_Chess"]["Selected"][0]] = GenerateChess()[jdata[f"{UserID}_Chess"]["Selected"][1]][jdata[f"{UserID}_Chess"]["Selected"][0]]
			if "♔" not in [jdata[f"{UserID}_Chess"]["Board"][y][x] for y in range(len(jdata[f"{UserID}_Chess"]["Board"])) for x in range(len(jdata[f"{UserID}_Chess"]["Board"][y]))] or "♚" not in [jdata[f"{UserID}_Chess"]["Board"][y][x] for y in range(len(jdata[f"{UserID}_Chess"]["Board"])) for x in range(len(jdata[f"{UserID}_Chess"]["Board"][y]))]:
				jdata[f"{UserID}_Chess"]["Selected"] = None
				jdata[f"{UserID}_Chess"]["Valid"] = []
				with open("JSON/Chess.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
				UpdateChess(UserID, [Coord[0], Coord[1]])
				del jdata[f"{UserID}_Chess"]
				with open("JSON/Chess.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
				Query.message.edit_media(media=InputMediaPhoto(open("Clients/Chess.png", "rb")))
				return os.remove("Clients/Chess.png")
			jdata[f"{UserID}_Chess"]["Player"] = not jdata[f"{UserID}_Chess"]["Player"]
		jdata[f"{UserID}_Chess"]["Selected"] = None
		jdata[f"{UserID}_Chess"]["Valid"] = []
	elif jdata[f"{UserID}_Chess"]["Selected"] == None and jdata[f"{UserID}_Chess"]["Board"][Coord[1]][Coord[0]] not in Player[jdata[f"{UserID}_Chess"]["Player"]]: return Query.bot.answer_callback_query(callback_query_id=Query.id, text="Invalid selection!")
	elif [Coord[0], Coord[1]] not in jdata[f"{UserID}_Chess"]["Valid"]: return Query.bot.answer_callback_query(callback_query_id=Query.id, text="Invalid move!")
	with open("JSON/Chess.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	Query.message.edit_media(reply_markup=UpdateChess(UserID), media=InputMediaPhoto(open("Clients/Chess.png", "rb")))
	os.remove("Clients/Chess.png")