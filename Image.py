from telegram import constants, InlineKeyboardButton, InlineKeyboardMarkup as Markup
import requests
import json

def Alarm(context):
	with open("JSON/Image.json", "r") as jfile: jdata = json.load(jfile)
	del jdata[f"{context.job.context}_Image"]
	with open("JSON/Image.json", "w") as jfile: json.dump(jdata, jfile, indent=2)

def Remove(context, Name):
	CurrentJob = context.job_queue.get_jobs_by_name(Name)
	if CurrentJob:
		for job in CurrentJob: job.schedule_removal()

def Keyboard(UserID, MsgID, Image): return Markup([[InlineKeyboardButton("⬅️", callback_data=f"Image,{UserID},{MsgID},{Image},Left"), InlineKeyboardButton("♻️", callback_data=f"Delete,{UserID}"), InlineKeyboardButton("➡️", callback_data=f"Image,{UserID},{MsgID},{Image},Right")]])

def Search(update, context):
	with open("JSON/Image.json", "r") as jfile: jdata = json.load(jfile)
	if len(context.args) > 0: Query = " ".join(context.args)
	else: return update.effective_message.reply_text("/search [Query]")
	MsgID = update.effective_message.message_id
	if Query in ["biology", "雨后小故事", "家教小故事", "blade of kibou"]: jdata[f"{MsgID}_Image"] = jdata[Query]
	else:
		Response = requests.get("https://rapidapi.p.rapidapi.com/api/Search/ImageSearchAPI", headers={"x-rapidapi-host": "contextualwebsearch-websearch-v1.p.rapidapi.com", "x-rapidapi-key": "bfac6d549cmsh56e8f9172fd3d87p107b51jsn1f4f055480fd"}, params={"q": Query, "pageNumber": 1, "pageSize": 10, "autoCorrect": True, "safeSearch": False}).json()
		jdata[f"{MsgID}_Image"] = [i["url"] for i in Response["value"]]
	with open("JSON/Image.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	context.job_queue.run_once(Alarm, 300, context=MsgID, name=f"{MsgID}_Image")
	update.effective_message.reply_text("Image [1]({URL})".format(URL=jdata[f"{MsgID}_Image"][0]), parse_mode=constants.PARSEMODE_MARKDOWN_V2, reply_markup=Keyboard(update.effective_user.id, MsgID, 0))

def SearchQuery(update, context):
	with open("JSON/Image.json", "r") as jfile: jdata = json.load(jfile)
	Query = update.callback_query
	Data = Query.data.split(",")
	MsgID = Data[2]
	Image = int(Data[3])
	Callback = Data[len(Data) - 1]
	if f"{MsgID}_Image" in jdata:
		if Callback == "Left":
			if Image - 1 >= 0: Image = Image - 1
			else: Image = Image + len(jdata[f"{MsgID}_Image"]) - 1
		elif Callback == "Right":
			if Image + 1 <= len(jdata[f"{MsgID}_Image"]) - 1: Image = Image + 1
			else: Image = 0
	else: return Query.edit_message_text(f"[Image]({Query.message.entities[0].url})", parse_mode=constants.PARSEMODE_MARKDOWN_V2)
	try:
		Remove(context, f"{MsgID}_Image")
		context.job_queue.run_once(Alarm, 300, context=MsgID, name=f"{MsgID}_Image")
		Query.edit_message_text("[Image {Image}]({URL})".format(Image=Image + 1, URL=jdata[f"{MsgID}_Image"][Image]), parse_mode=constants.PARSEMODE_MARKDOWN_V2, reply_markup=Keyboard(Data[1], MsgID, Image))
	except Exception as Error: Query.bot.answer_callback_query(callback_query_id=Query.id, text=Error, show_alert=True)