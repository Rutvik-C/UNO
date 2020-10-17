import itertools
import random


def peek(s):
    return s[-1]


a = ('0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9', '+2', '+2', 'Skip',
     'Skip', 'Reverse', 'Reverse')
color = ['Blue', 'Red', 'Green', 'Yellow']
deck1 = list(itertools.product(a, color))
for i in range(4):
    deck1.append(('Wild', 'Black'))
    deck1.append(('+4', 'Black'))
random.shuffle(deck1)
deck2 = list()
deck2.append(deck1.pop())

p1 = list()
p2 = list()
p3 = list()
p4 = list()
player_list = [p1, p2, p3, p4]
for i in range(4):
    for j in range(7):
        player_list[i].append(deck1.pop())
for i in range(4):
    print("P", i + 1, ":", sep="")
    for j in player_list[i]:
        print(j)
    print()

current = peek(deck2)
print("\nCurrent card:", current)

position = 0
direction_check = 1

if current[0] == 'Reverse':
    direction_check *= -1
elif current[0] == 'Skip':
    print("P1 skipped!")
    position = 1
elif current[1] == 'Black':
    new_color = random.choice(color)
    print("Color changes to:", new_color)
    current = (current[0], new_color)

while len(p1) != 0 and len(p2) != 0 and len(p3) != 0 and len(p4) != 0:
    played_check = 0
    check = 0
    if current[0] == '+2' or current[0] == '+4':
        for _ in range(2):
            try:
                player_list[position].append(deck1.pop())
            except:
                deck1, deck2 = deck2, deck1
                random.shuffle(deck1)
                player_list[position].append(deck1.pop())
        print("Draw", current[0])
        if current[0] == '+4':
            for _ in range(2):
                try:
                    player_list[position].append(deck1.pop())
                except:
                    deck1, deck2 = deck2, deck1
                    random.shuffle(deck1)
                    player_list[position].append(deck1.pop())
        played_check = 1
        current = ("", current[1])

    if played_check == 0:
        for item in player_list[position]:
            if current[1] in item or current[0] in item:
                print("\nP", position + 1, " played:", item, sep="")
                deck2.append(item)
                current = peek(deck2)
                if current[1] == 'Black':
                    new_color = random.choice(color)
                    print("Color changes to:", new_color)
                    current = (current[0], new_color)
                player_list[position].remove(item)
                check = 1
                break
        if check == 0:
            black_check = 0
            for item in player_list[position]:
                if 'Black' in item:
                    print("\nP", position + 1, " played:", item, sep="")
                    deck2.append(item)
                    current = peek(deck2)
                    new_color = random.choice(color)
                    print("Color changes to:", new_color)
                    current = (current[0], new_color)
                    player_list[position].remove(item)
                    black_check = 1
                    break
            if black_check == 0:
                print("Draw1")
                try:
                    player_list[position].append(deck1.pop())
                except:
                    deck1, deck2 = deck2, deck1
                    random.shuffle(deck1)
                    player_list[position].append(deck1.pop())
        if len(player_list[position]) == 1:
            print("UNO!")
    print("P", position + 1, ":")
    for i in player_list[position]:
        print(i)
    print("\nCurrent card:", current)
    if current[0] == 'Reverse':
        print("Direction reversed!")
        direction_check *= -1
        current = ("", current[1])
    if current[0] == 'Skip':
        if direction_check == 1:
            position += 1
            if position > 3:
                position = 0
        else:
            position -= 1
            if position < 0:
                position = 3
        print("P", position + 1, " skipped!")
        current = ("", current[1])
    if direction_check == 1:
        position += 1
        if position > 3:
            position = 0
    else:
        position -= 1
        if position < 0:
            position = 3

if len(p1) == 0:
    winner = 1
elif len(p2) == 0:
    winner = 2
elif len(p3) == 0:
    winner = 3
else:
    winner = 4
print("Winner is P", winner)
