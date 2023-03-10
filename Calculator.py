from telegram import InlineKeyboardButton, InlineKeyboardMarkup as Markup
from Handler import Edit
import json

def Scientific(UserID):
	with open("JSON/Calculator.json", "r") as jfile: jdata = json.load(jfile)
	Cal = jdata[f"{UserID}_Calculator"]
	if Cal["Scientific"]:
		Structure = ["^", ["lg", "đ¤"], ["ln", "đĢ"], "(", ")", "â", "ÂŠī¸", "đ", "%", ["â", "Ãˇ"], ["âī¸", "!"], ["7ī¸âŖ", "7"], ["8ī¸âŖ", "8"], ["9ī¸âŖ", "9"], ["âī¸", "Ã"], ["-1", "đ"], ["4ī¸âŖ", "4"], ["5ī¸âŖ", "5"], ["6ī¸âŖ", "6"], ["âķ Ĩķ Ĩ", "-"], "Ī", ["1ī¸âŖ", "1"], ["2ī¸âŖ", "2"], ["3ī¸âŖ", "3"], ["â", "+"], "đ", ["e", "đĸ"], ["0ī¸âŖ", "0"], ["âē", "."], "âī¸"]
		Length = 5
		if Cal["Inverse"]: Structure = ["2nd", None, ["sin-1", "đŧ"], ["cos-1", "đŦ"], ["tan-1", "đŊ"]] + Structure
		else: Structure = ["2nd", None, ["sin", "đ"], ["cos", "đ¸"], ["tan", "đ"]] + Structure
	else:
		Structure = ["ÂŠī¸", "đ", "%", ["â", "Ãˇ"], ["7ī¸âŖ", "7"], ["8ī¸âŖ", "8"], ["9ī¸âŖ", "9"], ["âī¸", "Ã"], ["4ī¸âŖ", "4"], ["5ī¸âŖ", "5"], ["6ī¸âŖ", "6"], ["âķ Ĩķ Ĩ", "-"], ["1ī¸âŖ", "1"], ["2ī¸âŖ", "2"], ["3ī¸âŖ", "3"], ["â", "+"], "đ",  ["0ī¸âŖ", "0"], ["âē", "."], "âī¸"]
		Length = 4
	Keyboard = []
	for a in [Structure[i:i + Length] for i in range(0, len(Structure), Length)]:
		Keyboard.append([])
		for b in a:
			if type(b) == list: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton(b[0], callback_data=f"Calculator,{UserID},{b[1]}"))
			elif b == None: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton("đĢ", callback_data="None"))
			else: Keyboard[len(Keyboard) - 1].append(InlineKeyboardButton(b, callback_data=f"Calculator,{UserID},{b}"))
	Keyboard.append([InlineKeyboardButton("âģī¸", callback_data=f"Delete,{UserID}")])
	if Cal["Query"] != "": Query = Cal["Query"].replace("đ", "sin(").replace("đ¸", "cos(").replace("đ", "tan(").replace("đŧ", "arcsin(").replace("đŦ", "arccos(").replace("đŊ", "arctan(").replace("đ¤", "lg(").replace("đĢ", "ln(").replace("â", "â(").replace("!", "!(").replace("đ", "^(-1)").replace("đĸ", "e")
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
	if a not in ["2nd", "ÂŠī¸", "đ", "%", "đ", "âī¸"]: Cal["Query"] += a
	elif a == "2nd": Cal["Inverse"] = not Cal["Inverse"]
	elif a == "ÂŠī¸": Cal["Query"] = Cal["Answer"] = ""
	elif a == "đ": Cal["Query"] = "".join(list(Cal["Query"])[:-1])
	elif a == "đ": Cal["Scientific"] = not Cal["Scientific"]
	elif a == "âī¸":
		if Cal["Query"] != "":
			try: Cal["Answer"] = str(eval(Cal["Query"].replace("đ", "m.sin(").replace("đ¸", "m.cos(").replace("đ", "m.tan(").replace("đŧ", "m.asin(").replace("đŦ", "m.acos(").replace("đŊ", "m.atan(").replace("^", "**").replace("đ¤","m.log10(").replace("đĢ","m.log(").replace("â", "m.sqrt(").replace("Ãˇ", "/").replace("!", "m.factorial(").replace("Ã", "*").replace("đ", "**(-1)").replace("Ī", "3.14159265").replace("đĸ", "2.71828183")))
			except: Cal["Answer"] = "Error"
		else: Cal["Answer"] = "0"
	with open("JSON/Calculator.json", "w") as jfile: json.dump(jdata, jfile, indent=2)
	Edit(Query, Scientific(UserID)[0], Markup(Scientific(UserID)[1]))