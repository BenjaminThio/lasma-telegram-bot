import requests
import json
import os

API_KEY = os.getenv('API_KEY')

def Weather(update, context):
	if len(context.args) > 0: Location = "".join([i for i in context.args])
	else: return update.effective_message.reply_text("/weather [Location]")
	try: Response = json.loads(requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={Location}&appid={API_KEY}&units=metric").content)
	except: return update.effective_message.reply_text(f"Invalid Location: {Location}")
	with open("Clients/Weather.png", "wb") as File: File.write(requests.get("http://openweathermap.org/img/wn/" + Response["weather"][0]["icon"] + "@2x.png").content)
	context.bot.send_photo(chat_id=update.effective_message.chat_id, photo=open("Clients/Weather.png", "rb"), caption=f"Weather Information For {Location}\nWeather: " + Response["weather"][0]["main"] + "\nDescription: " + Response["weather"][0]["description"] + f"\n\nOther Information For {Location}\nPressure: " + str(Response["main"]["pressure"]) + "hPa\nHumidity: " + str(Response["main"]["humidity"]) + "%\nWind Speed: " + str(Response["wind"]["speed"]) + "metre/sec\nWind Degrees: " + str(Response["wind"]["deg"]) + "°\nLongtitude: " + str(Response["coord"]["lon"]) + "\nLatitude: " + str(Response["coord"]["lat"]) + f"\n\nQuery from {update.effective_user.username}")
	os.remove("Clients/Weather.png")

def Temperature(update, context):
	if len(context.args) > 0: Location = "".join([i for i in context.args])
	else: return update.effective_message.reply_text("/temp [Location]")
	try: Response = json.loads(requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={Location}&appid={API_KEY}&units=metric").content)
	except: return update.effective_message.reply_text(f"Invalid Location: {Location}")
	update.effective_message.reply_text("Temperature Informations For {Location}\nTemperature: {0}\nTemperature/Min: {1}\nTemperature/Max: {2}\nFeels Like: {3}\n\nQuery by {Username}".format(Location=Location, *[f"{i}°C / {round(float(i) + 273.15, 2)}°K / {round((float(i) * 9 / 5) + 32, 2)}°F" for i in [Response['main']['temp'], Response['main']['temp_min'], Response['main']['temp_max'], Response['main']['feels_like']]], Username=update.effective_user.username))