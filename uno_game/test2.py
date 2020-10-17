import itertools
import random

p1 = list()
p2 = list()
p3 = list()
p4 = list()
player_list = [p1, p2, p3, p4]
deck1 = list()
deck2 = list()
direction_check = 1
position = 0
current = list()
special_check = 0

color = ['Blue', 'Red', 'Green', 'Yellow']


def peek(s):
    return s[-1]


def create():
    global current, deck2, deck1, color
    a = ('0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9', '+2', '+2', 'Skip', 'Skip', 'Reverse', 'Reverse')
    deck1 = list(itertools.product(a, color))
    for i in range(4):
        deck1.append(('Wild', 'Black'))
        deck1.append(('+4', 'Black'))
    random.shuffle(deck1)
    deck2.append(deck1.pop())
    for i in range(4):
        for j in range(7):
            player_list[i].append(deck1.pop())
    current = deck2[-1]


def action():
    global deck1, deck2, current, special_check
    special_check = 0
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
        if current[0] == '+4' and special_check == 0:
            for _ in range(2):
                try:
                    player_list[position].append(deck1.pop())
                except:
                    deck1, deck2 = deck2, deck1
                    random.shuffle(deck1)
                    player_list[position].append(deck1.pop())
        played_check = 1
        special_check = 1

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
                    special_check = 0
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
                new_card = ()
                try:
                    new_card = (deck1.pop())
                except:
                    deck1, deck2 = deck2, deck1
                    random.shuffle(deck1)
                    new_card = (deck1.pop())
                if new_card[1] == 'Black':
                    print("\nP", position + 1, " played:", new_card, sep="")
                    new_color = random.choice(color)
                    print("Color changes to:", new_color)
                    current = (new_card[0], new_color)
                    special_check = 0
                elif new_card[1] == current[1]:
                    print("\nP", position + 1, " played:", new_card, sep="")
                    deck2.append(new_card)
                    special_check = 0
                elif new_card[0] == current[0]:
                    print("\nP", position + 1, " played:", new_card, sep="")
                    deck2.append(new_card)
                    special_check = 0
                else:
                    player_list[position].append(new_card)
        if len(player_list[position]) == 1:
            print("UNO!")


def get_curr_player():
    global direction_check, current, position, special_check
    if current[0] == 'Reverse' and special_check == 0:
        direction_check *= -1
        special_check = 1
    if current[0] == 'Skip' and special_check == 0:
        special_check = 1
        position = (position + direction_check) % 4
    position = (position + direction_check) % 4
    return position


def user_action(_type, card):
    if _type == 0:  # Card played!
        pass
        # Card is a tuple eg. ("4", "Red")
        # Check if it's a valid move
        # If valid change globals if special handle it and return True if played successfully
        # Return False if Invalid move

    if _type == 1:  # Taken from stack
        pass
        # Card will be None
        # Check if it's valid move
        # If valid, change globals and return True
        # Return False if Invalid move


