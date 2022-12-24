from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from PyDictionary import PyDictionary
from gtts import gTTS
import json
import os

def Dictionary(update, context):
	with open("JSON/Voice.json", "r") as jfile: jdata = json.load(jfile)
	UserID = update.effective_user.id
	if f"{UserID}_Voice" not in jdata: jdata[f"{UserID}_Voice"] = {"Language": "en"}
	with open("JSON/Voice.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	if len(context.args) > 0: Query = context.args[0].title()
	else: return update.effective_message.reply_text("/d [Query]")
	Meanings = PyDictionary(Query).getMeanings()
	Username = update.effective_user.username
	String = ""
	reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("♻️", callback_data=f"Delete,{update.effective_user.id}")]])
	for a in ["Noun", "Adjective", "Verb", "Adverb"]:
		try:
			if a in Meanings[Query]: String += f"\n{a}\n"
		except: return update.effective_message.reply_text(f"Query: {Query}\n\n• Word Not Found!\n\nQuery from {Username}", reply_markup=reply_markup)
		try: String += "\n".join([f"• {b}" for b in Meanings[Query][a]]) + "\n"
		except: continue
	gTTS(text=Query, lang=jdata[f"{update.effective_user.id}_Voice"]["Language"]).save("Clients/Dictionary.ogg")
	context.bot.send_voice(chat_id=update.effective_message.chat_id, voice=open("Clients/Dictionary.ogg", "rb"), caption=f"Query: {Query}\n{String}\nQuery from {Username}", reply_markup=reply_markup)
	os.remove("Clients/Dictionary.ogg")