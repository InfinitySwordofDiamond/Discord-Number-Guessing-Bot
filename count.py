from plyer import notification
from pygame import mixer
import requests
import time
import json
import random
import emoji
import re
import os

authToken = {"authorization": "Your discord token"}																				# <--- Change
responses = ["List", "of", "messages", "that", "will", "respond", "to", "a", "ping"]											# <--- Change
win, alert, notWorking, sus, nameMentioned = "win.wav", "alert.wav", "notworking.wav", "sus.wav", "namementioned.wav"
userID, channelID = "Your Discord ID", "The channel ID to guess the number"														# <--- Change
botID, botDMID = "ID of the bot that is sending the messages", "If the bot DMs you and you have to reply with a message"		# <--- Change
numberList, randomNumbers = [], []
restart, requestContinue = True, False
startNumber = endNumber = runs = 0
textFileName = "numbers.txt"
loadMessageLimit = 100
mixer.init()

def notify(message):
	notification.notify(
		title = "Discord Bot",
		message = message,
		app_icon = os.path.dirname(__file__) + "\\discordbot.ico",
		timeout = 10,
	)


def notificationBanner(warningMessage, soundFile, message):
	print(warningMessage, "\n")
	notify(message)
	mixer.music.load(os.path.dirname(__file__) + f"\\{soundFile}")
	mixer.music.play()


def yesNo(text):
	while True:
		choice = input(text)
		print()

		if (choice.lower() == "y" or choice.lower() == "yes"):
			return True

		elif (choice.lower() == "n" or choice.lower() == "no"):
			return False
		
		print("Please type in (Y / N) or (Yes / No)\n")


def intInput(text, int1, int2):
	while True:
		try:
			number = int(input(text))
		
		except:
			print("\nPlease type in a valid answer\n")
			continue

		if (int1 <= number <= int2):
			return number

		elif number == -1:
			print()
			return -1

		else:
			print("\nEnter a number between (", int1, " - ", int2, ") or -1 to Restart\n", sep="")


def pause():
	print("Paused Program...\n")
	next = input("Type \"1\" to continue / Type a key to exit\n")
	print()
	
	if next == '1':
		print("Resuming Program...\n")
		return 1

	else:
		return 0


def request(option, ID, message, messageID, reaction):
	offline = False

	while True:
		try:
			if option == "get":
				getMessageInfo = json.loads(requests.get(f"https://discord.com/api/v9/channels/{ID}/messages?limit={loadMessageLimit}", headers=authToken).text)
				if offline: print("Reconnected...\n")
				return getMessageInfo

			if option == "post":
				requests.post(f"https://discord.com/api/v9/channels/{ID}/messages", json={'content': message}, headers=authToken)

			if option == "delete":
				requests.delete(f"https://discord.com/api/v9/channels/{ID}/messages/{messageID}/reactions/{emoji.emojize(reaction)}/%40me", headers=authToken)
			
			if offline: print("Reconnected...\n")
			break

		except:
			pass
		
		if not offline: print("You are offline...\n")
		offline = True


def detectMessages():
	messageInfo = request("get", channelID, None, None, None)
	generalChannel = request("get", "The general channel ID of the server to check for pings", None, None, None)			# <--- Change
	ping = win = ignore = noBotResponse = warning = 0

	while ping < 10:
		randomInt = random.randint(0, len(responses) - 1)

		if (f'<@{userID}>' in messageInfo[ping]['content'] or f'{userID}' in ''.join(str(text) for text in messageInfo[ping]['mentions'])):
			text = "The message if you have been pinged by someone"															# <--- Change
			notificationBanner(text, alert, text)
			time.sleep(3)
			request("post", channelID, responses[randomInt], None, None)
			return 0

		if (f'<@{userID}>' in generalChannel[ping]['content']):
			text = "The message if you have been pinged by someone"															# <--- Change
			notificationBanner(text, alert, text)
			time.sleep(3)
			request("post", "The general channel ID of the server to respond a ping", responses[randomInt], None, None)		# <--- Change
			return 0 

		ping += 1
	
	while win < 8:
		if ("Winning message of the Bot" in messageInfo[win]['content'] and f"{botID}" in str(messageInfo[win]['author'])):	# <--- Change
			messageInfoDM = request("get", f"{botDMID}", None, None, None)

			if ("Bot message when they DM you that you won the game" in messageInfoDM[0]['content']):						# <--- Change
				request("post", f"{botDMID}", "Responding message to the bot DM", None, None)								# <--- Change

			elif ("Alternative message of the bot when it DMs you" in messageInfoDM[0]['content']):							# <--- Change
				request("post", f"{botDMID}", "Responding message to the bot DM", None, None)								# <--- Change

			return 1

		win += 1

	while ignore < 7:
		if not ("Message to check that is constantly sent by the bot when it is functioning" in messageInfo[ignore]['content']):				# <--- Change
			noBotResponse += 1

		ignore += 1

	if (noBotResponse == 7):
		return 2

	while warning < 6:
		pause = ''.join(str(text) for text in (messageInfo[warning]))

		if ("bot" in messageInfo[warning]['content'] or "hack" in messageInfo[warning]['content'] or "auto" in messageInfo[warning]['content']):
			return 3

		if ("Short version of your Discord Username" in messageInfo[warning]['content']):									# <--- Change
			return 4

		if ("timestampflagscomponentsreactions" in pause):
			return 5
		
		warning += 1


def reviewMessages(usedNumbersList, allNumbersList, messageAmount):
	messagesInfo = request("get", channelID, None, None, None)
	messageCounter = 0
	
	while messageCounter < messageAmount:
		try:
			if ("Message to stop looking for messages after it detects the message" in messagesInfo[messageCounter]['content'] and f"{botID}" in str(messagesInfo[messageCounter]['author'])): break		# <--- Change

			if not messagesInfo[messageCounter]['content'].isdigit():
				messageCounter += 1
				continue

			selectedNumber = int(''.join(messagesInfo[messageCounter]['content']))

		except:
			messageCounter += 1
			continue

		if not (0 <= selectedNumber <= 500):
			messageCounter += 1
			continue

		try:
			usedNumbersList.append(selectedNumber)
			usedNumbersList = [*set(usedNumbersList)]
			allNumbersList.remove(selectedNumber)

		except ValueError: pass
		messageCounter += 1

	return usedNumbersList, allNumbersList


def processCount(allNumbers):
	success = False
	usedNumbers = []
	
	with open(os.path.dirname(__file__) + f"\\{textFileName}") as readFile: numbers = readFile.read()
	usedNumbers = [int(number) for number in (numbers.strip("[]")).split(', ') if number.isdigit()]
		
	if usedNumbers:
		if yesNo("Do you want to clear used numbers list? (Y / N): "):
			open(os.path.dirname(__file__) + f"\\{textFileName}", "w").close()
			usedNumbers = []

	usedNumbers, allNumbers = reviewMessages(usedNumbers, allNumbers, 1000)

	while (0 < len(allNumbers) - 1):
		usedNumbers, allNumbers = reviewMessages(usedNumbers, allNumbers, 20)
		with open(os.path.dirname(__file__) + f"\\{textFileName}", "w") as file: file.write(str(usedNumbers))

		for usedNumber in usedNumbers:
			try: 
				allNumbers.remove(usedNumber)

			except ValueError:
				pass
			

		if (success and not allNumbers):
			notify("Message when the bot finishes counting")																# <--- Change
			break

		elif (not allNumbers):
			print("All the numbers have been typed\n")																		
			break

		request("post", channelID, allNumbers[0], None, None)

		success = True
		time.sleep(7)

		if (detectMessages() == 0): break
		
		if (detectMessages() == 1):
			text = "Message when someone has found the number"																# <--- Change
			notificationBanner(text, win, text)
			open(os.path.dirname(__file__) + f"\\{textFileName}", "w").close()
			usedNumbers = allNumbers = []
			return 1
		
		if (detectMessages() == 2):
			text = "Message when the bot isn't functioning"																	# <--- Change
			notificationBanner(text, notWorking, text)
			break

		if (detectMessages() == 3):
			text = "Message when someone says the word hack, auto, or bot"													# <--- Change
			notificationBanner(text, sus, text)

		if (detectMessages() == 4):
			text = "Message when someone mentions your Discord Username but doesn't ping you"								# <--- Change							
			notificationBanner(text, nameMentioned, text)

		if (detectMessages() == 5):
			counter = 0

			while counter < 6:
				reaction = ''.join([re.sub(r'[^\U00010000-\U0010ffff]', '', str(request("get", channelID, None, None, None)[counter]))])
				messageID = request("get", channelID, None, None, None)[counter]['id']
				request("delete", channelID, None, messageID, reaction)
				counter += 1

			if pause() == 0: break
		
		time.sleep(3)
		if len(allNumbers) == 1: notify("Message when the bot finishes counting")											# <--- Change


class runProgram():
	try:
		with open(os.path.dirname(__file__) + f"\\{textFileName}", "x") as file: file.write("")
	
	except: pass

	while restart:
		randomNumber = yesNo("Random Numbers? (Y / N): ")
		requestContinue = breakLoop = False

		if randomNumber:
			if (0 < len(randomNumbers) - 1 and not (runs == 0)):
				requestContinue = yesNo("Do you want to continue from previous list? (Y / N): ")

				if randomNumber:
					smallNumber = 0
					bigNumber = 500

			if not requestContinue:
				while True:
					smallNumber = intInput("Small Number (Low Number - High Number) or -1 to Restart: ", "Low Number", "High Number")													# <--- Change

					if smallNumber == -1:
						breakLoop = True
						break

					bigNumber = intInput("Big Number (Low Number + 1 - High Number) or -1 to Restart [Must be bigger than the small number]: ", "Low Number + 1", "High Number")		# <--- Change

					if bigNumber == -1:
						breakLoop = True
						break

					print()

					if smallNumber > bigNumber:
						print("The small number must be smaller than the big number\n")
						continue

					break

				if breakLoop:
					continue

			if smallNumber < bigNumber:
				if not requestContinue:
					randomNumbers = list(range(smallNumber, bigNumber + 1))
					random.shuffle(randomNumbers)
				
				randomNumberList = ", ".join(str(number) for number in randomNumbers)
				print("Random Number List: [" + randomNumberList + "]\n")

				if processCount(randomNumbers) == 1: randomNumbers, numberList = [], []

		else:
			if (0 < len(numberList) - 1 and not (runs == 0)):
				requestContinue = yesNo("Do you want to continue from previous list? (Y / N): ")

				if requestContinue:
					startNumber = 0
					endNumber = 500
					stepCount = 1
			
			if not requestContinue:
				while True:
					startNumber = intInput("Starting Number (Low Number - High Number) or -1 to Restart: ", "Low Number", "High Number")			# <--- Change

					if startNumber == -1:
						breakLoop = True
						break

					endNumber = intInput("Ending Number (Low Number - High Number) or -1 to Restart: ", "Low Number", "High Number")				# <--- Change

					if endNumber == -1:
						breakLoop = True
						break
					
					stepCount = intInput("Step Count (Low Number + 1 - High Number) or -1 to Restart: ", "Low Number + 1", "High Number")			# <--- Change

					if stepCount == -1:
						breakLoop = True
						break

					print()

					if (startNumber == endNumber):
						print("The starting number cannot equal the ending number\n")
						continue
					
					numberList = []
					break

				if breakLoop:
					continue

			count = startNumber

			if startNumber < endNumber:
				while (count <= endNumber and not requestContinue):
					numberList.append(count)
					count += stepCount

			elif startNumber > endNumber:
				while (count >= endNumber and not requestContinue):
					numberList.append(count)
					count -= stepCount		
					
			numbersList = ", ".join(str(number) for number in numberList)
			print("Number List: [" + numbersList + "]\n")

			if processCount(numberList) == 1: numberList, randomNumbers = [], []

		restart = yesNo("Restart? (Y / N): ")
		mixer.music.stop()
		runs += 1