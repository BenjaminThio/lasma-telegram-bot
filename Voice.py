from telegram import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
import speech_recognition as sr
from pydub import AudioSegment
from Handler import Edit
import gtts
import json
import os

def Voice(update, context):
	with open("JSON/Voice.json", "r") as jfile: jdata = json.load(jfile)
	UserID = update.effective_user.id
	if f"{UserID}_Voice" not in jdata: jdata[f"{UserID}_Voice"] = {"Language": "en", "srLang": "English (United States)"}
	with open("JSON/Voice.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	if len(context.args) < 1: return update.effective_message.reply_text("/s [Sentences]")
	gtts.gTTS(text=" ".join([i for i in context.args]), lang=jdata[f"{UserID}_Voice"]["Language"]).save("Clients/Voice.ogg")
	context.bot.send_voice(chat_id=update.effective_message.chat_id, voice=open("Clients/Voice.ogg", "rb"), reply_markup=Markup([[Button("♻️", callback_data=f"Delete,{update.effective_user.id}")]]))
	os.remove("Clients/Voice.ogg")

def UpdateSettings(update, context):
	with open("JSON/Voice.json", "r") as jfile: jdata = json.load(jfile)
	UserID = update.effective_user.id
	if f"{UserID}_Voice" not in jdata: jdata[f"{UserID}_Voice"] = {"Language": "en", "srLang": "English (United States)"}
	with open("JSON/Voice.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	Available = gtts.lang.tts_langs()
	Languages = [i for i in Available]
	Languages.remove(jdata[f"{UserID}_Voice"]["Language"])
	Length = 5
	Keyboard = []
	for a in [Languages[i:i + Length] for i in range(0, len(Languages), Length)]:
		Keyboard.append([])
		for b in a: Keyboard[len(Keyboard) - 1].append(Button(f"{Available[b]}", callback_data=f"Voice,{UserID},{b}"))
	Keyboard.append([Button("♻️", callback_data=f"Delete,{UserID}")])
	return ["Languages: " + jdata[f"{UserID}_Voice"]["Language"], Markup(Keyboard)]

def Settings(update, context): update.effective_message.reply_text(UpdateSettings(update, context)[0], reply_markup=UpdateSettings(update, context)[1])

def SettingsQuery(update, context):
	with open("JSON/Voice.json", "r") as jfile: jdata = json.load(jfile)
	Query = update.callback_query
	Data = Query.data.split(",")
	UserID = Data[1]
	jdata[f"{UserID}_Voice"]["Language"] = Data[-1]
	with open("JSON/Voice.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	Edit(Query, UpdateSettings(update, context)[0], UpdateSettings(update, context)[1])

def SpeechRecognition(update, context):
	with open("JSON/Voice.json", "r") as jfile: jdata = json.load(jfile)
	chatId = update.effective_message.chat_id
	userId = update.effective_user.id
	try:
		audio = context.bot.get_file(update.effective_message.reply_to_message.voice.file_id)
		audio.download("Clients/Audio.ogg")
	except:
		context.bot.send_message(chat_id=chatId, text="Reply to somebody's voice message with /sr")
		return
	try:
		downloadedAudio = AudioSegment.from_ogg("Clients/Audio.ogg")
		downloadedAudio.export("Clients/Audio.wav", format="wav")
		os.remove("Clients/Audio.ogg")
	except Exception as error:
		context.bot.send_message(chat_id=chatId, text=error)
		os.remove("Clients/Audio.ogg")
		return
	recognizer = sr.Recognizer()
	try:
		audioFile = sr.AudioFile("Clients/Audio.wav")
		with audioFile as source:
			audioFile = recognizer.record(source)
			convertedText = recognizer.recognize_google(audioFile, language=GetLanguageCode(jdata[f"{userId}_Voice"]["srLang"]))
			context.bot.send_message(chat_id=chatId, text=convertedText)
	except Exception as error:
		context.bot.send_message(chat_id=chatId, text=error)
	os.remove("Clients/Audio.wav")

def Language(update, context):
	with open("JSON/Voice.json", "r") as jfile: jdata = json.load(jfile)
	userId = update.effective_user.id
	with open("JSON/Lang.json", "r") as langFile: langData = json.load(langFile)
	langsCode = langData["languagesCode"]
	if f"{userId}_Voice" not in jdata: jdata[f"{userId}_Voice"] = {"Language": "en", "srLang": "English (United States)"}
	with open("JSON/Voice.json", "w") as jfile: json.dump(jdata, jfile , indent=2)
	message = f"Default language: {jdata[f'{userId}_Voice']['srLang']}"
	keyboard = [
			[
				Button("🔽", callback_data=f"Language,{userId},Down")
			],
			[
				Button("♻️", callback_data=f"Delete,{userId}")
			]
		]
	if len(context.args) == 0:
		update.effective_message.reply_text(message, reply_markup=Markup(keyboard))
	elif len(context.args) > 0:
		if not context.args[0].isdigit():
			update.effective_message.reply_text(f"Only positive integer is allowed for the argument, Do /lang for more info.")
			return
		if int(context.args[0]) <= 0 or int(context.args[0]) > len(langsCode):
			update.effective_message.reply_text(f"The number given should be greater than or equal to 1 and lesser than or equal to {len(langsCode)}, Do /lang for more info.")
			return
		if list(langsCode)[int(context.args[0]) - 1] == jdata[f"{userId}_Voice"]["srLang"]:
			update.effective_message.reply_text("You are using the language already.")
			return
		jdata[f"{userId}_Voice"]["srLang"] = list(langsCode)[int(context.args[0]) - 1]
		with open("JSON/Voice.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
		update.effective_message.reply_text(f"{message} ➡️ {jdata[f'{userId}_Voice']['srLang']}", reply_markup=Markup(keyboard))

def GetLanguageCode(language):
	with open("JSON/Lang.json", "r") as langFile: langData = json.load(langFile)
	return langData["languagesCode"][language]

def LanguageQuery(update, context):
	with open("JSON/Voice.json", "r") as jfile: jdata = json.load(jfile)
	with open("JSON/Lang.json", "r") as langFile: langData = json.load(langFile)
	query = update.callback_query
	data = query.data.split(",")
	userId = data[1]
	callback = data[2]
	with open("JSON/Voice.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	message = f"Default language: {jdata[f'{userId}_Voice']['srLang']}"
	keyboard = []
	if callback == "Down":
		langsCode = langData["languagesCode"]
		message += "\n\nLanguages available:\n" + "\n".join([f"{i + 1}. {list(langsCode.keys())[i]}" for i in range(len(langsCode))]) + f"\n\nDo /lang [Number of languages available above]\n*Note: The number given should be greater than or equal to 1 and lesser than or equal to {len(langsCode)}."
		keyboard = [
			[
				Button("🔼", callback_data=f"Language,{userId},Up")
			],
			[
				Button("♻️", callback_data=f"Delete,{userId}")
			]
		]
	elif callback == "Up":
		keyboard = [
			[
				Button("🔽", callback_data=f"Language,{userId},Down")
			],
			[
				Button("♻️", callback_data=f"Delete,{userId}")
			]
		]
	Edit(query, message, Markup(keyboard))