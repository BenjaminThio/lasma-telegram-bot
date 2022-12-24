from telegram import InlineKeyboardButton, InlineKeyboardMarkup as Markup, InputMediaPhoto
from PIL import Image, ImageDraw
import json
import os

Width = 8
Height = 8
Color = {"Red": "🟥", "Orange": "🟧", "Yellow": "🟨", "Green": "🟩", "Blue": "🟦", "Purle": "🟪", "Black": "⬛️", "White": "⬜️", "Brown": "🟫"}

def UpdateDraw(UserID):
	with open("JSON/Draw.json", "r") as jfile: jdata = json.load(jfile)
	Keyboard = []
	Location = [0, 0]
	for a in range(len(jdata[f"{UserID}_Draw"]["Board"])):
		b = [i for i in jdata[f"{UserID}_Draw"]["Board"][a]]
		Keyboard.append([InlineKeyboardButton(b[c], callback_data=f"Draw,{UserID},{c}:{a}") for c in range(len(b))])
	IMG = Image.new("RGB", (Width * 100, Height * 100))
	for a in jdata[f"{UserID}_Draw"]["Board"]:
		for b in a:
			for c in Color:
				if Color[c] == b: ImageDraw.Draw(IMG).rectangle([(Location[0] * 100, Location[1] * 100), ((Location[0] + 100) * 100, (Location[1] + 100) * 100)], fill = c)
			Location[0] += 1
		Location[0] = 0
		Location[1] += 1
	IMG.save("Clients/Draw.png")
	return Keyboard

def Draw(update, context):
	with open("JSON/Draw.json", "r") as jfile: jdata = json.load(jfile)
	UserID = update.effective_user.id
	jdata[f"{UserID}_Draw"] = {"Board": [[Color["White"]] * Width for b in range(Height)]}
	with open("JSON/Draw.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	context.bot.send_photo(chat_id=update.effective_message.chat_id, reply_markup=Markup(UpdateDraw(UserID)), photo=open("Clients/Draw.png", "rb"))
	os.remove("Clients/Draw.png")

def DrawQuery(update, context):
	with open("JSON/Draw.json", "r") as jfile: jdata = json.load(jfile)
	Query = update.callback_query
	Data = Query.data.split(",")
	UserID = Data[1]
	Location = Data[-1].split(":")
	jdata[f"{UserID}_Draw"]["Board"][int(Location[1])][int(Location[0])] = Color["Red"]
	with open("JSON/Draw.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	try: Query.message.edit_media(reply_markup=Markup(UpdateDraw(UserID)), media=InputMediaPhoto(open("Clients/Draw.png", "rb")))
	except Exception as Error: Query.bot.answer_callback_query(callback_query_id=Query.id, text=Error, show_alert=True)
	os.remove("Clients/Draw.png")