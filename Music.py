import re
import requests
from pytube import YouTube
from urllib.parse import quote
from urllib.request import urlopen
from youtube_transcript_api import YouTubeTranscriptApi
from telegram import InlineKeyboardButton, InlineKeyboardMarkup as Markup
from Handler import Edit
import os

def Music(update, context):
	UserID = update.effective_user.id
	ChatID = update.effective_message.chat_id
	Keyboard = [[InlineKeyboardButton("♻️", callback_data=f"Delete,{UserID}")]]
	if len(context.args) > 0: Query = " ".join([f"{i}" for i in context.args])
	else: return update.effective_message.reply_text("/p [Title]")
	Searching = context.bot.send_message(chat_id=ChatID, text=f"Searching related audios...")
	try: HTML = urlopen(f"https://www.youtube.com/results?search_query={quote(Query)}")
	except: context.bot.edit_message_text(chat_id=ChatID, message_id=Searching.message_id, text="Audio not found!")
	VideoIDs = re.findall(r"watch\?v=(\S{11})", HTML.read().decode())
	for i in range(5):
		URL = YouTube(f"https://www.youtube.com/watch?v={VideoIDs[i]}")
		Keyboard.insert(i, [InlineKeyboardButton("Preview", url=URL.thumbnail_url), InlineKeyboardButton(URL.title, callback_data=f"Music,{UserID},{VideoIDs[i]}")])
	context.bot.edit_message_text(chat_id=ChatID, message_id=Searching.message_id, text=f"Results for {Query.title()}", reply_markup=Markup(Keyboard))

def MusicQuery(update, context):
	Query = update.callback_query
	Data = Query.data.split(",")
	UserID = Data[1]
	Choice = Data[-1]
	Name = update.effective_user.name
	ChatID = update.effective_message.chat_id
	Limit = 3600
	Video = f"https://www.youtube.com/watch?v={Choice}"
	URL = YouTube(Video)
	Keyboard = [[InlineKeyboardButton("♻️", callback_data=f"Delete,{UserID}")]]
	if URL.length <= Limit + 300:
		Sending = Edit(Query, "Sending audio...")
		try: Output = URL.streams.filter(only_audio=True).first().download("Clients")
		except Exception as Error: return Edit(Query, Error)	
		os.rename(Output, "Clients/Music.mp3")
		try: Captions = "\n".join([i["text"] for i in YouTubeTranscriptApi.get_transcript(Choice, languages=[i.language_code for i in YouTubeTranscriptApi.list_transcripts(Choice)])])
		except: Captions = "Subtitles were disabled for this video!\n"
		context.bot.send_voice(chat_id=ChatID, voice=open("Clients/Music.mp3", "rb"), caption=f"Title: {URL.title}\nLength: {URL.length} secs\nQuery from: {Name}", reply_markup=Markup(Keyboard))
		Sending.delete()
		with open("Clients/Thumbnail.png", "wb") as File: File.write(requests.get(URL.thumbnail_url).content)
		Keyboard[len(Keyboard) - 1].insert(0, InlineKeyboardButton("📼", url=Video))
		try: context.bot.send_photo(chat_id=ChatID, photo=open("Clients/Thumbnail.png", "rb"), caption=f"Captions:\n{Captions}", reply_markup=Markup(Keyboard))
		except:
			Keyboard[len(Keyboard) - 1].insert(0, InlineKeyboardButton("🖼", url=URL.thumbnail_url))
			with open("Clients/Captions.txt", "w") as File: File.write(f"Captions:\n{Captions}")
			context.bot.send_document(chat_id=ChatID, document=open("Clients/Captions.txt", "rb"), reply_markup=Markup(Keyboard))
			os.remove("Clients/Captions.txt")
		os.remove("Clients/Thumbnail.png")
		os.remove("Clients/Music.mp3")
	else: context.bot.send_message(chat_id=ChatID, text=f"Audio length: {URL.length} secs, please find an audio less than {Limit} secs[{int(Limit / 60)} mins]!")