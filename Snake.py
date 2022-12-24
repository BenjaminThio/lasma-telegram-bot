from telegram import InlineKeyboardButton, InlineKeyboardMarkup as Markup, InputMediaPhoto
from PIL import Image
from Handler import EditMedia
import random
import json
import os

Width = 5
Height = 5
Head = "🤢"
Body = "🟢"
Food = "🍎"
Barrier = "⬛️"
Background = "⬜️"

def UpdateSnake(UserID):
	with open("JSON/Snake.json", "r") as jfile: jdata = json.load(jfile)
	String = ""
	IMG = Image.new("RGB", ((Width + 2) * 50, (Height + 2) * 50), color="White")
	for y in range(Height + 2):
		for x in range(Width + 2): IMG.paste(Image.open(f"Snake/{Barrier}.png"), (x * 50, y * 50), mask=Image.open(f"Snake/{Barrier}.png"))
	for y in range(len(jdata[f"{UserID}_Snake"]["World"])):
		for x in range(len(jdata[f"{UserID}_Snake"]["World"][y])):
			IMG.paste(Image.open(f"Snake/{Background}.png"), ((x + 1) * 50, (y + 1) * 50), mask=Image.open(f"Snake/{Background}.png"))
			IMG.paste(Image.open(f"Snake/{jdata[f'{UserID}_Snake']['World'][y][x]}.png"), ((x + 1) * 50, (y + 1) * 50), mask=Image.open(f"Snake/{jdata[f'{UserID}_Snake']['World'][y][x]}.png"))
			String += jdata[f"{UserID}_Snake"]["World"][y][x]
		String += f"{Barrier}\n{Barrier}"
	IMG.save("Clients/Snake.png")
	return ["".join([Barrier * (Width + 1), f"{Barrier}\n{Barrier}{String}", Barrier * (Width + 1)]), Markup([[InlineKeyboardButton("⬆️", callback_data=f"Snake,{UserID},Up")], [InlineKeyboardButton("⬅️", callback_data=f"Snake,{UserID},Left"), InlineKeyboardButton("🔄", callback_data=f"Snake,{UserID},Reshuffle"), InlineKeyboardButton("➡️", callback_data=f"Snake,{UserID},Right")], [InlineKeyboardButton("⬇️", callback_data=f"Snake,{UserID},Down")]])]

def Reshuffle(UserID):
	with open("JSON/Snake.json", "r") as jfile: jdata = json.load(jfile)
	Coordinates = [[a, b] for a in range(Width) for b in range(Height)]
	Coords = [Coordinates.pop(random.choice([i for i in range(len(Coordinates))])) for i in range(2)]
	jdata[f"{UserID}_Snake"] = {"Head": Coords.pop(0),"Body": [], "World": [[Background] * Width for i in range(Height)]}
	j = jdata[f"{UserID}_Snake"]
	j["World"][j["Head"][1]][j["Head"][0]] = Head
	j["World"][Coords[0][1]][Coords[0][0]] = Food
	with open("JSON/Snake.json", "w") as jfile: json.dump(jdata, jfile, indent=2)

def Snake(update, context):
	with open("JSON/Snake.json", "r") as jfile: jdata = json.load(jfile)
	UserID = update.effective_user.id
	if f"{UserID}_Snake" not in jdata: Reshuffle(UserID)
	context.bot.send_photo(chat_id=update.effective_message.chat_id, reply_markup=UpdateSnake(UserID)[1], photo=open("Clients/Snake.png", "rb"))
	os.remove("Clients/Snake.png")

def SnakeQuery(Query):
	with open("JSON/Snake.json", "r") as jfile: jdata = json.load(jfile)
	Data = Query.data.split(",")
	UserID = Data[1]
	Callback = Data[len(Data) - 1]
	if f"{UserID}_Snake" not in jdata: return Query.message.edit_media(media=InputMediaPhoto(open("Images/GameOver.png", "rb")))
	j = jdata[f"{UserID}_Snake"]
	j["World"][j["Head"][1]][j["Head"][0]] = Body
	j["Body"].insert(0, [j["Head"][0], j["Head"][1]])
	if Callback == "Left":
		if j["Head"][0] - 1 < 0: j["Head"][0] += Width - 1
		elif j["Head"][0] - 1 >= 0: j["Head"][0] -= 1
	elif Callback == "Right":
		if j["Head"][0] + 1 >= Width: j["Head"][0] = 0
		elif j["Head"][0] + 1 < Width: j["Head"][0] += 1
	elif Callback == "Up":
		if j["Head"][1] - 1 < 0: j["Head"][1] += Height - 1
		elif j["Head"][1] - 1 >= 0: j["Head"][1] -= 1
	elif Callback == "Down":
		if j["Head"][1] + 1 >= Height: j["Head"][1] = 0
		elif j["Head"][1] + 1 < Height: j["Head"][1] += 1
	elif Callback == "Reshuffle":
		Reshuffle(UserID)
		return EditMedia(Query, UpdateSnake(UserID)[1], "Snake")
	if j["World"][j["Head"][1]][j["Head"][0]] != Food:
		j["World"][j["Body"][-1][1]][j["Body"][-1][0]] = Background
		del j["Body"][-1]
	else:
		Available = []
		for a in range(Width):
			for b in range(Height):
				if j["World"][b][a] != Food and [a, b] not in j["Body"]: Available.append([a, b])
		if len(Available) > 0:
			Coord = random.choice(Available)
			j["World"][Coord[1]][Coord[0]] = Food
		else:
			Query.message.edit_media(media=InputMediaPhoto(open("Images/GameOver.png", "rb")))
			del jdata[f"{UserID}_Snake"]
			with open("JSON/Snake.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
			return
	j["World"][j["Head"][1]][j["Head"][0]] = Head
	for i in j["Body"]: j["World"][i[1]][i[0]] = Body
	if j["World"][j["Head"][1]][j["Head"][0]] == Body:
		Query.message.edit_media(media=InputMediaPhoto(open("Images/GameOver.png", "rb")))
		del jdata[f"{UserID}_Snake"]
		with open("JSON/Snake.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
		return
	with open("JSON/Snake.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	EditMedia(Query, UpdateSnake(UserID)[1], "Snake")