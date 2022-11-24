from count import reviewMessages, detectMessages, textFileName
import os

try:
    with open(os.path.dirname(__file__) + f"\\{textFileName}", "x") as file: file.write("")

except: pass

removedNumber = None

while True:
    numbersUsed, dummyList = [], []

    with open(os.path.dirname(__file__) + f"\\{textFileName}") as readFile: numbers = readFile.read()
    numbersUsed = [int(number) for number in (numbers.strip("[]")).split(', ') if number.isdigit()]

    numbersUsed, dummyList, removedNumber = reviewMessages(numbersUsed, dummyList, 100, removedNumber)
    with open(os.path.dirname(__file__) + f"\\{textFileName}", "w") as file: file.write(str(numbersUsed))

    if (detectMessages() == 1):
        open(os.path.dirname(__file__) + f"\\{textFileName}", "w").close()
        print("\nThe number has been found so " + textFileName + "has been cleared\n")
        numbersUsed = []