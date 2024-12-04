import random
import string
import math

ROW_SIZE = 11

class Finger():
    def __init__(self, currKeyIndex, possibleKeys):
        self.currKeyIndex = currKeyIndex
        self.possibleKeys = possibleKeys + [currKeyIndex] 

def associateCharsWithKeys():
    characteres = string.ascii_lowercase + "ç,.´~"
    letterToIndex = {letter: index for index, letter in enumerate(characteres)}
    letterToIndex['^'] = letterToIndex['~']
    letterToIndex['`'] = letterToIndex['´']
    return letterToIndex


def findingBestFinger(fingers, keyIndexToPress):
    for finger in fingers:
        if keyIndexToPress in finger.possibleKeys:
            return finger

def initializeFingers():
    fingerA = Finger(11, [0, 22])
    fingerS = Finger(12, [1, 23])
    fingerD = Finger(13, [2, 24])
    fingerF = Finger(14, [3, 25, 4, 15, 26])

    fingerJ = Finger(17, [5, 16, 27, 6, 28])
    fingerK = Finger(18, [7, 29])
    fingerL = Finger(19, [8, 30])
    fingerÇ = Finger(20, [9, 30, 10, 21])

    return [fingerA, fingerS, fingerD, fingerF, fingerJ, fingerK, fingerL, fingerÇ]

def charCost(keyboard, letter):
    cost = 0
    letterToIndex = associateCharsWithKeys()
    fingers = initializeFingers()

    letterIndexInKeyboard = keyboard.index(letterToIndex[letter])

    choosenFinger = findingBestFinger(fingers, letterIndexInKeyboard)
    
    currLetterPos = indexToCoordinates(letterIndexInKeyboard)
    fingerPos = indexToCoordinates(choosenFinger.currKeyIndex)
    
    choosenFinger.currKeyIndex = letterIndexInKeyboard

    cost += math.dist(currLetterPos, fingerPos)

    return cost

def indexToCoordinates(index):
    row = index // ROW_SIZE
    col = index % ROW_SIZE

    offset = 0
    if index >= ROW_SIZE and index < 2 * ROW_SIZE:
        offset = 0.25
    elif index >= 2 * ROW_SIZE:
        offset = 0.75

    x = col + offset
    y = row 

    return (x, y)

def isKeyboardValid(keyboard):
    seen = set()

    for key in keyboard:
        if key in seen:
            return False
        seen.add(key)

    return True

standardKeyboard = [16, 22, 4, 17, 19, 24, 20, 8, 14, 15, 29,
                     0, 18, 3, 5,   6, 7, 9, 10, 11, 26, 30,
                      25, 23, 2, 21,  1, 13,12,27, 28]
