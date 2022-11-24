from count import reviewMessages, request, textFileName, channelID, botID
import time
import os

try:
    with open(os.path.dirname(__file__) + f"\\{textFileName}", "x") as file: file.write("")

except: pass

def checkMessages():
    messageInfo = request("get", channelID, None, None, None)
    count = 0

    while count < 4:
        if ("Winning Message" in messageInfo[count]['content'] and f"{botID}" in str(messageInfo[count]['author'])):                    # <--- Change
            return 1

removedNumber = None

while True:
    numbersUsed, dummyList = [], []

    with open(os.path.dirname(__file__) + f"\\{textFileName}") as readFile: numbers = readFile.read()
    numbersUsed = [int(number) for number in (numbers.strip("[]")).split(', ') if number.isdigit()]

    numbersUsed, dummyList, removedNumber = reviewMessages(numbersUsed, dummyList, 100, removedNumber)
    with open(os.path.dirname(__file__) + f"\\{textFileName}", "w") as file: file.write(str(numbersUsed))

    if (checkMessages() == 1):
        open(os.path.dirname(__file__) + f"\\{textFileName}", "w").close()
        print("\nThe number has been found so " + textFileName + "has been cleared\n")
        numbersUsed = []
        time.sleep(20)