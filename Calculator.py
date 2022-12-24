from telegram import InlineKeyboardButton, InlineKeyboardMarkup as Markup
from Handler import Edit
import json

def Scientific(UserID):
	with open("JSON/Calculator.json", "r") as jfile: jdata = json.load(jfile)
	Cal = jdata[f"{UserID}_Calculator"]
	if Cal["Scientific"]:
		Structure = ["^", ["lg", "𝔤"], ["ln", "𝔫"], "(", ")", "√", "©️", "🔙", "%", ["➗", "÷"], ["❗️", "!"], ["7️⃣", "7"], ["8️⃣", "8"], ["9️⃣", "9"], ["✖️", "×"], ["-1", "𝖓"], ["4️⃣", "4"], ["5️⃣", "5"], ["6️⃣", "6"], ["➖󠀥󠀥", "-"], "π", ["1️⃣", "1"], ["2️⃣", "2"], ["3️⃣", "3"], ["➕", "+"], "🔄", ["e", "𝔢"], ["0️⃣", "0"], ["⏺", "."], "✔️"]
		Length = 5
		if Cal["Inverse"]: Structure = ["2nd", None, ["sin-1", "𝓼"], ["cos-1", "𝓬"], ["tan-1", "𝓽"]] + Structure
		else: Structure = ["2nd", None, ["sin", "𝓈"], ["cos", "𝒸"], ["tan", "𝓉"]] + Structure
	else:
		Structure = ["©️", "🔙", "%", ["➗", "÷"], ["7️⃣", "7"], ["8️⃣", "8"], ["9️⃣", "9"], ["✖️", "×"], ["4️⃣", "4"], ["5️⃣", "5"], ["6️⃣", "6"], ["➖󠀥󠀥", "-"], ["1️⃣", "1"], ["2️⃣", "2"], ["3️⃣", "3"], ["➕", "+"], "🔄",  ["0️⃣", "0"], ["⏺", "."], "✔️"]
		Length = 4
	Keyboard = []
	for a in [Structure[i:i + Length] for i in range(0, len(Structure), Length)]:
		Keyboard.append([])
		for b in a:
			if type(b) == list: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton(b[0], callback_data=f"Calculator,{UserID},{b[1]}"))
			elif b == None: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton("🚫", callback_data="None"))
			else: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton(b, callback_data=f"Calculator,{UserID},{b}"))
	Keyboard.append([InlineKeyboardButton("♻️", callback_data=f"Delete,{UserID}")])
	if Cal["Query"] != "": Query = Cal["Query"].replace("𝓈", "sin(").replace("𝒸", "cos(").replace("𝓉", "tan(").replace("𝓼", "arcsin(").replace("𝓬", "arccos(").replace("𝓽", "arctan(").replace("𝔤", "lg(").replace("𝔫", "ln(").replace("√", "√(").replace("!", "!(").replace("𝖓", "^(-1)").replace("𝔢", "e")
	else: Query = "0"
	if Cal["Answer"] != "": Answer = Cal["Answer"]
	else: Answer = "0"
	return [{False: "", True: "Scientific "}[Cal["Scientific"]] + f"Calculator\nQuery: {Query}\nAnswer: {Answer}", Keyboard]

def Calculator(update, context):
	with open("JSON/Calculator.json", "r") as jfile: jdata = json.load(jfile)
	UserID = update.effective_user.id
	if f"{UserID}_Calculator" not in jdata: jdata[f"{UserID}_Calculator"] = {"Query": "", "Answer": "", "Scientific": False, "Inverse": False}
	with open("JSON/Calculator.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	update.effective_message.reply_text(Scientific(UserID)[0], reply_markup=Markup(Scientific(UserID)[1]))

def CalculatorQuery(Query):
	with open("JSON/Calculator.json", "r") as jfile: jdata = json.load(jfile)
	Data = Query.data.split(",")
	UserID = Data[1]
	a = Data[len(Data) - 1]
	Cal = jdata[f"{UserID}_Calculator"]
	if a not in ["2nd", "©️", "🔙", "%", "🔄", "✔️"]: Cal["Query"] += a
	elif a == "2nd": Cal["Inverse"] = not Cal["Inverse"]
	elif a == "©️": Cal["Query"] = Cal["Answer"] = ""
	elif a == "🔙": Cal["Query"] = "".join(list(Cal["Query"])[:-1])
	elif a == "🔄": Cal["Scientific"] = not Cal["Scientific"]
	elif a == "✔️":
		if Cal["Query"] != "":
			try: Cal["Answer"] = str(eval(Cal["Query"].replace("𝓈", "m.sin(").replace("𝒸", "m.cos(").replace("𝓉", "m.tan(").replace("𝓼", "m.asin(").replace("𝓬", "m.acos(").replace("𝓽", "m.atan(").replace("^", "**").replace("𝔤","m.log10(").replace("𝔫","m.log(").replace("√", "m.sqrt(").replace("÷", "/").replace("!", "m.factorial(").replace("×", "*").replace("𝖓", "**(-1)").replace("π", "3.14159265").replace("𝔢", "2.71828183")))
			except: Cal["Answer"] = "Error"
		else: Cal["Answer"] = "0"
	with open("JSON/Calculator.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	Edit(Query, Scientific(UserID)[0], Markup(Scientific(UserID)[1]))