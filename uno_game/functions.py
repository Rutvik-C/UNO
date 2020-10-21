import itertools
import random

winner = -1
player_playing = False
play_lag = -1


def peek(s):
    return s[-1]


def create(ob):
    a = ('0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9',
         '+2', '+2', 'Skip', 'Skip', 'Reverse', 'Reverse')
    ob.deck1 = list(itertools.product(a, ob.color))
    for _ in range(4):
        ob.deck1.append(('Wild', 'Black'))
        ob.deck1.append(('+4', 'Black'))
    random.shuffle(ob.deck1)

    while peek(ob.deck1) in [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Skip', 'Green'), ('Skip', 'Blue'),
                             ('Skip', 'Yellow'), ('Reverse', 'Red'), ('Reverse', 'Green'), ('Reverse', 'Blue'),
                             ('Reverse', 'Yellow'), ('+2', 'Red'), ('+2', 'Green'), ('+2', 'Blue'),
                             ('+2', 'Yellow')]:
        random.shuffle(ob.deck1)

    ob.deck2.append(ob.deck1.pop())
    ob.current = ob.deck2[-1]

    for j in range(1, 4):
        for _ in range(7):
            ob.player_list[j].append(ob.deck1.pop())

    ob.player_list[0].append(("Reverse", "Red"))
    ob.player_list[0].append(("Reverse", "Yellow"))
    ob.player_list[0].append(("Reverse", "Blue"))
    ob.player_list[0].append(("Reverse", "Green"))
    ob.player_list[0].append(("Skip", "Red"))
    ob.player_list[0].append(("Skip", "Yellow"))
    ob.player_list[0].append(("Skip", "Blue"))
    ob.player_list[0].append(("Skip", "Green"))


def set_curr_player(ob, default):
    if ob.current[0] == 'Reverse' and ob.special_check == 0:
        ob.direction_check *= -1
        ob.special_check = 1
    if ob.current[0] == 'Skip' and ob.special_check == 0:
        ob.special_check = 1
        ob.position = (ob.position + ob.direction_check) % 4

    if default:
        ob.position = (ob.position + ob.direction_check) % 4


def is_empty(x):
    if len(x) == 0:
        return True

    return False


def re_initialize(ob):
    global winner, player_playing, play_lag
    winner = -1
    player_playing = False
    play_lag = -1
    ob.p1 = list()
    ob.p2 = list()
    ob.p3 = list()
    ob.p4 = list()
    ob.player_list = [ob.p1, ob.p2, ob.p3, ob.p4]
    ob.deck1 = list()
    ob.deck2 = list()
    ob.direction_check = 1
    ob.position = -1
    ob.special_check = 0
    ob.current = list()

    # Dealing the cards
    create(ob)


def take_from_stack(ob):
    if not ob.drawn:
        ob.player_list[0].append(ob.deck1.pop())
        ob.drawn = True


def play_this_card(ob, card):
    if not ob.played:
        if card[0] == ob.current[0] or card[1] == ob.current[1]:
            print("Player played ->", card, "\n")
            ob.played, ob.drawn = True, True
            ob.deck2.append(card)
            ob.current = peek(ob.deck2)
            ob.p1.remove(ob.current)
            ob.special_check = 0
            set_curr_player(ob, False)

        if card[1] == 'Black':
            ob.played, ob.drawn = True, True
            new_color = input()
            print("new color is:", new_color)
            ob.p1.remove(card)
            card = (card[0], new_color)
            ob.deck2.append(card)
            ob.current = peek(ob.deck2)
            ob.special_check = 0


def bot_action(ob):
    print("Bot called ->", ob.position)
    ob.played_check = 0
    ob.check = 0
    if ob.current[0] == '+2' and ob.special_check == 0:
        for _ in range(2):
            try:
                ob.player_list[ob.position].append(ob.deck1.pop())
            except:
                ob.deck1, ob.deck2 = ob.deck2, ob.deck1
                random.shuffle(ob.deck1)
                ob.player_list[ob.position].append(ob.deck1.pop())
        print("Draw", ob.current[0])
        ob.played_check = 1
        ob.special_check = 1
    if ob.current[0] == '+4' and ob.special_check == 0:
        for _ in range(4):
            try:
                ob.player_list[ob.position].append(ob.deck1.pop())
            except:
                ob.deck1, ob.deck2 = ob.deck2, ob.deck1
                random.shuffle(ob.deck1)
                ob.player_list[ob.position].append(ob.deck1.pop())
        ob.played_check = 1
        ob.special_check = 1

    if ob.played_check == 0:
        check = 0
        for item in ob.player_list[ob.position]:
            if ob.current[1] in item or ob.current[0] in item:
                print("P", ob.position, " played:", item, sep="")
                ob.special_check = 0
                ob.deck2.append(item)
                ob.current = peek(ob.deck2)
                if ob.current[1] == 'Black':
                    new_color = random.choice(ob.color)
                    print("Color changes to:", new_color)
                    ob.current = (ob.current[0], new_color)
                ob.player_list[ob.position].remove(item)
                check = 1
                break

        if check == 0:
            black_check = 0
            for item in ob.player_list[ob.position]:
                if 'Black' in item:
                    print("P", ob.position, " played:", item, sep="")
                    ob.special_check = 0
                    ob.deck2.append(item)
                    ob.current = peek(ob.deck2)
                    new_color = random.choice(ob.color)
                    print("Color changes to:", new_color)
                    ob.current = (ob.current[0], new_color)
                    ob.player_list[ob.position].remove(item)
                    black_check = 1
                    break
            if black_check == 0:
                print("Draw1")
                try:
                    new_card = (ob.deck1.pop())
                except:
                    ob.deck1, ob.deck2 = ob.deck2, ob.deck1
                    random.shuffle(ob.deck1)
                    new_card = (ob.deck1.pop())
                if new_card[1] == 'Black':
                    print("P", ob.position, " played:", new_card, sep="")
                    new_color = random.choice(ob.color)
                    print("Color changes to:", new_color)
                    ob.current = (new_card[0], new_color)
                    ob.special_check = 0
                elif new_card[1] == ob.current[1] or new_card[0] == ob.current[0]:
                    print("P", ob.position, " played:", new_card, sep="")
                    ob.deck2.append(new_card)
                    ob.special_check = 0
                else:
                    ob.player_list[ob.position].append(new_card)
        if len(ob.player_list[ob.position]) == 1:
            print("UNO!")
