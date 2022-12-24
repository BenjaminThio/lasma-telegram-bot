from telegram import InputMediaPhoto
import os

def Edit(Query, Text, Keyboard=None):
	try:
		if Keyboard != None: return Query.edit_message_text(Text, reply_markup=Keyboard)
		else: return Query.edit_message_text(Text)
	except Exception as Error: Query.bot.answer_callback_query(callback_query_id=Query.id, text=Error, show_alert=True)

def EditMedia(Query, Markup, Base):
	Query.message.edit_media(reply_markup=Markup, media=InputMediaPhoto(open(f"Clients/{Base}.png", "rb")))
	os.remove(f"Clients/{Base}.png")
	return

def Delete(Query):
	try: Query.message.delete()
	except Exception as Error: Query.bot.answer_callback_query(callback_query_id=Query.id, text=Error, show_alert=True)