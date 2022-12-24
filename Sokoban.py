from telegram import InlineKeyboardButton, InlineKeyboardMarkup as Markup, InputMediaPhoto
from PIL import Image
from Handler import EditMedia
import random
import json
import os

Width = 7
Height = 5
Player = "🤡"
Barrier = "⬛️"
Background = "⬜️"
Box = "📦"
Destination = "❌"

def RandomCoord(Quantity):
	Coordinates = [[a, b] for a in range(Width) for b in range(Height)]
	return [Coordinates.pop(random.choice([i for i in range(len(Coordinates))])) for i in range(Quantity)]

def UpdateSokoban(UserID):
	with open("JSON/Sokoban.json", "r") as jfile: jdata = json.load(jfile)
	String = ""
	IMG = Image.new("RGB", ((Width + 2) * 50, (Height + 2) * 50), color="White")
	for y in range(Height + 2):
		for x in range(Width + 2): IMG.paste(Image.open(f"Sokoban/{Barrier}.png"), (x * 50, y * 50), mask=Image.open(f"Sokoban/{Barrier}.png"))
	for y in range(len(jdata[f"{UserID}_Sokoban"]["World"])):
		for x in range(len(jdata[f"{UserID}_Sokoban"]["World"][y])):
			IMG.paste(Image.open(f"Sokoban/{Background}.png"), ((x + 1) * 50, (y + 1) * 50), mask=Image.open(f"Sokoban/{Background}.png"))
			IMG.paste(Image.open(f"Sokoban/{jdata[f'{UserID}_Sokoban']['World'][y][x]}.png"), ((x + 1) * 50, (y + 1) * 50), mask=Image.open(f"Sokoban/{jdata[f'{UserID}_Sokoban']['World'][y][x]}.png"))
			String += jdata[f"{UserID}_Sokoban"]["World"][y][x]
		String += f"{Barrier}\n{Barrier}"
	IMG.save("Clients/Sokoban.png")
	return ["".join([Barrier * (Width + 1), f"{Barrier}\n{Barrier}{String}", Barrier * (Width + 1)]), Markup([[InlineKeyboardButton("⬆️", callback_data=f"Sokoban,{UserID},Up")], [InlineKeyboardButton("⬅️", callback_data=f"Sokoban,{UserID},Left"), InlineKeyboardButton("🔄", callback_data=f"Sokoban,{UserID},Reshuffle"), InlineKeyboardButton("➡️", callback_data=f"Sokoban,{UserID},Right")], [InlineKeyboardButton("⬇️", callback_data=f"Sokoban,{UserID},Down")]])]

def Reshuffle(UserID):
	with open("JSON/Sokoban.json", "r") as jfile: jdata = json.load(jfile)
	Coords = RandomCoord(10)
	jdata[f"{UserID}_Sokoban"] = {"Player": Coords.pop(0), "Destinations": [Coords.pop(0) for i in range(3)], "World": [[Background] * Width for i in range(Height)]}
	j = jdata[f"{UserID}_Sokoban"]
	j["World"][j["Player"][1]][j["Player"][0]] = Player
	for i in [Coords.pop(0) for i in range(3)]: j["World"][i[1]][i[0]] = Barrier
	for i in [Coords.pop(0) for i in range(3)]: j["World"][i[1]][i[0]] = Box
	for i in j["Destinations"]: j["World"][i[1]][i[0]] = Destination
	with open("JSON/Sokoban.json", "w") as jfile: json.dump(jdata, jfile, indent=2)

def Sokoban(update, context):
	with open("JSON/Sokoban.json", "r") as jfile: jdata = json.load(jfile)
	UserID = update.effective_user.id
	if f"{UserID}_Sokoban" not in jdata: Reshuffle(UserID)
	context.bot.send_photo(chat_id=update.effective_message.chat_id, reply_markup=UpdateSokoban(UserID)[1], photo=open("Clients/Sokoban.png", "rb"))
	os.remove("Clients/Sokoban.png")

def SokobanQuery(Query):
	with open("JSON/Sokoban.json", "r") as jfile: jdata = json.load(jfile)
	Data = Query.data.split(",")
	UserID = Data[1]
	Callback = Data[len(Data) - 1]
	if f"{UserID}_Sokoban" not in jdata: return Query.message.edit_media(media=InputMediaPhoto(open("Images/GameOver.png", "rb")))
	j = jdata[f"{UserID}_Sokoban"]
	j["World"][j["Player"][1]][j["Player"][0]] = Background
	if Callback == "Left":
		if j["Player"][0] - 2 >= 0 and j["World"][j["Player"][1]][j["Player"][0] - 1] == Box and j["World"][j["Player"][1]][j["Player"][0] - 2] in [Barrier, Box]: return
		elif j["Player"][0] - 1 >= 0 and j["Player"][0] - 2 < 0 and j["World"][j["Player"][1]][j["Player"][0] - 1] == Box and j["World"][j["Player"][1]][j["Player"][0] + Width - 2] in [Barrier, Box]: return
		elif j["Player"][0] - 1 < 0 and j["World"][j["Player"][1]][j["Player"][0] + Width - 1] == Box and j["World"][j["Player"][1]][j["Player"][0] + Width - 2] in [Barrier, Box]: return
		if j["Player"][0] - 1 < 0 and j["World"][j["Player"][1]][j["Player"][0] + Width - 1] not in [Barrier, Destination]: j["Player"][0] += Width - 1
		elif j["Player"][0] - 1 >= 0 and j["World"][j["Player"][1]][j["Player"][0] - 1] not in [Barrier, Destination]: j["Player"][0] -= 1
		else: return
		if j["Player"][0] - 1 < 0 and j["World"][j["Player"][1]][j["Player"][0]] == Box: j["World"][j["Player"][1]][j["Player"][0] + Width - 1] = Box
		elif j["Player"][0] - 1 >= 0 and j["World"][j["Player"][1]][j["Player"][0]] == Box: j["World"][j["Player"][1]][j["Player"][0] - 1] = Box
	elif Callback == "Right":
		if j["Player"][0] + 2 < Width and j["World"][j["Player"][1]][j["Player"][0] + 1] == Box and j["World"][j["Player"][1]][j["Player"][0] + 2] in [Barrier, Box]: return
		elif j["Player"][0] + 1 < Width and j["Player"][0] + 2 >= Width and j["World"][j["Player"][1]][j["Player"][0] + 1] == Box and j["World"][j["Player"][1]][0] in [Barrier, Box]: return
		elif j["Player"][0] + 1 >= Width and j["World"][j["Player"][1]][0] == Box and j["World"][j["Player"][1]][1] in [Barrier, Box]: return
		if j["Player"][0] + 1 >= Width and j["World"][j["Player"][1]][0] not in [Barrier, Destination]: j["Player"][0] = 0
		elif j["Player"][0] + 1 < Width and j["World"][j["Player"][1]][j["Player"][0] + 1] not in [Barrier, Destination]: j["Player"][0] += 1
		else: return
		if j["Player"][0] + 1 >= Width and j["World"][j["Player"][1]][j["Player"][0]] == Box: j["World"][j["Player"][1]][0] = Box
		elif j["Player"][0] + 1 < Width and j["World"][j["Player"][1]][j["Player"][0]] == Box: j["World"][j["Player"][1]][j["Player"][0] + 1] = Box
	elif Callback == "Up":
		if j["Player"][1] - 2 >= 0 and j["World"][j["Player"][1] - 1][j["Player"][0]] == Box and j["World"][j["Player"][1] - 2][j["Player"][0]] in [Barrier, Box]: return
		elif j["Player"][1] - 1 >= 0 and j["Player"][1] - 2 < 0 and j["World"][j["Player"][1] - 1][j["Player"][0]] == Box and j["World"][j["Player"][1] + Height - 2][j["Player"][0]] in [Barrier, Box]: return
		elif j["Player"][1] - 1 < 0 and j["World"][j["Player"][1] + Height - 1][j["Player"][0]] == Box and j["World"][j["Player"][1] + Height - 2][j["Player"][0]] in [Barrier, Box]: return
		if j["Player"][1] - 1 < 0 and j["World"][j["Player"][1] + Height - 1][j["Player"][0]] not in [Barrier, Destination]: j["Player"][1] += Height - 1
		elif j["Player"][1] - 1 >= 0 and j["World"][j["Player"][1] - 1][j["Player"][0]] not in [Barrier, Destination]: j["Player"][1] -= 1
		else: return
		if j["Player"][1] - 1 < 0 and j["World"][j["Player"][1]][j["Player"][0]] == Box: j["World"][j["Player"][1] + Height - 1][j["Player"][0]] = Box
		elif j["Player"][1] - 1 >= 0 and j["World"][j["Player"][1]][j["Player"][0]] == Box: j["World"][j["Player"][1] - 1][j["Player"][0]] = Box
	elif Callback == "Down":
		if j["Player"][1] + 2 < Height and j["World"][j["Player"][1] + 1][j["Player"][0]] == Box and j["World"][j["Player"][1] + 2][j["Player"][0]] in [Barrier, Box]: return
		elif j["Player"][1] + 1 < Height and j["Player"][1] + 2 >= Height and j["World"][j["Player"][1] + 1][j["Player"][0]] == Box and j["World"][0][j["Player"][0]] in [Barrier, Box]: return
		elif j["Player"][1] + 1 >= Height and j["World"][0][j["Player"][0]] == Box and j["World"][1][j["Player"][0]] in [Barrier, Box]: return
		if j["Player"][1] + 1 >= Height and j["World"][0][j["Player"][0]] not in [Barrier, Destination]: j["Player"][1] = 0
		elif j["Player"][1] + 1 < Height and j["World"][j["Player"][1] + 1][j["Player"][0]] not in [Barrier, Destination]: j["Player"][1] += 1
		else: return
		if j["Player"][1] + 1 >= Height and j["World"][j["Player"][1]][j["Player"][0]] == Box: j["World"][0][j["Player"][0]] = Box
		elif j["Player"][1] + 1 < Height and j["World"][j["Player"][1]][j["Player"][0]] == Box: j["World"][j["Player"][1] + 1][j["Player"][0]] = Box
	elif Callback == "Reshuffle":
		Reshuffle(UserID)
		return EditMedia(Query, UpdateSokoban(UserID)[1], "Sokoban")
	j["World"][j["Player"][1]][j["Player"][0]] = Player
	for i in j["Destinations"]:
		if j["World"][i[1]][i[0]] == Box:
			j["World"][i[1]][i[0]] = Barrier
			j["Destinations"].pop(j["Destinations"].index(i))
	if len(j["Destinations"]) == 0:
		del jdata[f"{UserID}_Sokoban"]
		with open("JSON/Sokoban.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
		return Query.message.edit_media(media=InputMediaPhoto(open("Images/GameOver.png", "rb")))
	with open("JSON/Sokoban.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	EditMedia(Query, UpdateSokoban(UserID)[1], "Sokoban")