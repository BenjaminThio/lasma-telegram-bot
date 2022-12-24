from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from Handler import Edit
import pytz

def Datetime(Timezone, Format): return datetime.now().astimezone(pytz.timezone(Timezone)).strftime(Format)

def Grouping():
	Timezones = pytz.all_timezones
	Width = 5
	Length = 10
	Groups = [Timezones[i:i + Width] for i in range(0, len(Timezones), Width)]
	return [Groups[i:i + Length] for i in range(0, len(Groups), Length)]

def Timezones(Group, Datetime, UserID):
	Keyboard = []
	for a in Grouping()[Group]:
		Keyboard.append([])
		for b in a:
			try: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton(b.split("/")[1], callback_data=f"{Datetime},{UserID},{b}"))
			except: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton(b, callback_data=f"Date,{UserID},{b}"))
	Keyboard.append([InlineKeyboardButton("⬅️", callback_data=f"{Datetime},{UserID},{Group},Left"), InlineKeyboardButton("♻️", callback_data=f"Delete,{UserID}"), InlineKeyboardButton("➡️", callback_data=f"{Datetime},{UserID},{Group},Right")])
	return InlineKeyboardMarkup(Keyboard)

def Date(update, context): update.effective_message.reply_text("Timezones 1", reply_markup=Timezones(0, "Date", update.effective_user.id))

def Time(update, context): update.effective_message.reply_text("Timezones 1", reply_markup=Timezones(0, "Time", update.effective_user.id))

def DatetimeQuery(Query, Service):
	Data = Query.data.split(",")
	UserID = Data[1]
	Timezone = Data[-1]
	if Timezone not in ["Left", "Right"]:
		if Service == "Date": Edit(Query, f"📆Date Today In {Timezone}📆\n\nDate: {Datetime(Timezone, '%d/%m/%Y')}\nDay: {Datetime(Timezone, '%A')}\n\nQuery by {Query.from_user.username}")
		elif Service == "Time": Edit(Query, f"⏰Time Now In {Timezone}⏰\n\nTime: {Datetime(Timezone, '%I:%M%p')}\nInternational Time: {Datetime(Timezone, '%H:%M')}\n\nQuery by {Query.from_user.username}")
	else:
		Group = int(Data[2])
		if Timezone == "Left":
			if Group - 1 >= 0: Group = Group - 1
			else: Group = Group + len(Grouping()) - 1
		elif Timezone == "Right":
			if Group + 1 <= len(Grouping()) - 1: Group = Group + 1
			else: Group = 0
		Edit(Query, f"Timezones {Group + 1}", Timezones(Group, Service, UserID))