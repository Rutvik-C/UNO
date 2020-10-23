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

    for i in range(3):
        while peek(ob.deck1) in [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Skip', 'Green'), ('Skip', 'Blue'),
                                 ('Skip', 'Yellow'), ('Reverse', 'Red'), ('Reverse', 'Green'), ('Reverse', 'Blue'),
                                 ('Reverse', 'Yellow'), ('+2', 'Red'), ('+2', 'Green'), ('+2', 'Blue'),
                                 ('+2', 'Yellow')]:
            random.shuffle(ob.deck1)

    ob.deck2.append(ob.deck1.pop())
    ob.current = ob.deck2[-1]

    for j in range(4):
        for _ in range(3):
            ob.player_list[j].append(ob.deck1.pop())

def set_curr_player(ob, default):
    if ob.current[0] == 'Reverse' and ob.special_check == 0:
        ob.direction_check *= -1
        ob.special_check = 1
    if ob.current[0] == 'Skip' and ob.special_check == 0:
        ob.special_check = 1
        ob.position = (ob.position + ob.direction_check) % 4

    if default:
        ob.position = (ob.position + ob.direction_check) % 4


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
            ob.player_list[0].remove(ob.current)
            ob.special_check = 0
            set_curr_player(ob, False)

        if card[1] == 'Black':
            ob.played, ob.drawn = True, True
            ob.choose_color = True
            ob.player_list[0].remove(card)
            print("In here")
            ob.deck2.append(card)


def play_this_card_2(ob, color):
    print("new color is:", color)
    print("In here 2")
    ob.deck2[-1] = (ob.deck2[-1][0], color)
    ob.current = peek(ob.deck2)
    ob.special_check = 0


def bot_action(ob):
    ob.message = ""
    ob.uno[ob.position] = False
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
    elif ob.current[0] == '+4' and ob.special_check == 0:
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
                print("1: P", ob.position, " played:", item, sep="")
                ob.special_check = 0

                ob.deck2.append(item)

                ob.current = peek(ob.deck2)

                if item[1] == 'Black':
                    ob.special_check = 0
                    ob.deck2.append(item)
                    ob.current = peek(ob.deck2)
                    if not ob.easy:
                        d = dict()
                        d['Blue'] = 0
                        d['Green'] = 0
                        d['Yellow'] = 0
                        d['Red'] = 0
                        d['Black'] = 0
                        for _item in ob.player_list[ob.position]:
                            d[_item[1]] += 1
                        d=sorted(d.items(), key = lambda kv:(kv[1], kv[0]))
                        new_color =d[-1][0]
                        print(d,new_color)
                        if new_color == 'Black':
                            new_color =d[-2][0]
                            print(d,new_color)
                    else:
                        new_color = random.choice(ob.color)
                    print("Color changes to:", new_color)
                    ob.message = "%s plays %s %s, new color is %s" % (
                        ob.bot_map[ob.position], item[0], item[1], new_color)
                    ob.current = (ob.current[0], new_color)

                ob.player_list[ob.position].remove(item)

                set_curr_player(ob, False)
                check = 1
                break

        if check == 0:
            black_check = 0
            for item in ob.player_list[ob.position]:
                if 'Black' in item:
                    print("2: P", ob.position, " played:", item, sep="")
                    ob.special_check = 0
                    ob.deck2.append(item)
                    ob.current = peek(ob.deck2)
                    if not ob.easy:
                        d = dict()
                        d['Blue'] = 0
                        d['Green'] = 0
                        d['Yellow'] = 0
                        d['Red'] = 0
                        d['Black'] = 0
                        for _item in ob.player_list[ob.position]:
                            d[_item[1]] += 1
                        d=sorted(d.items(), key = lambda kv:(kv[1], kv[0]))
                        new_color =d[-1][0]
                        print(d,new_color)
                        if new_color == 'Black':
                            new_color = d[-2][0]
                            print(d,new_color)
                    else:
                        new_color = random.choice(ob.color)

                    # new_color = random.choice(ob.color)  # comment this and uncomment previous
                    print("Color changes to:", new_color)

                    ob.message = "%s plays %s, new color is %s" % (ob.bot_map[ob.position], item[0], new_color)

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
                    print("3: P", ob.position, " played:", new_card, sep="")
                    if not ob.easy:
                        d = dict()
                        d['Blue'] = 0
                        d['Green'] = 0
                        d['Yellow'] = 0
                        d['Red'] = 0
                        d['Black'] = 0
                        for _item in ob.player_list[ob.position]:
                            d[_item[1]] += 1
                        d=sorted(d.items(), key = lambda kv:(kv[1], kv[0]))
                        new_color =d[-1][0]
                        print(d,new_color)
                        if new_color == 'Black':
                            new_color = d[-2][0]
                            print(d,new_color)
                    else:
                        new_color = random.choice(ob.color)
                    # new_color = random.choice(ob.color)  # comment this and uncomment previous
                    print("Color changes to:", new_color)
                    ob.message = "%s plays %s, new color is %s" % (ob.bot_map[ob.position], new_card[0], new_color)

                    ob.current = (new_card[0], new_color)
                    ob.special_check = 0
                elif new_card[1] == ob.current[1] or new_card[0] == ob.current[0]:
                    print("P", ob.position, " played:", new_card, sep="")
                    ob.deck2.append(new_card)
                    ob.current = new_card
                    set_curr_player(ob, False)
                    ob.special_check = 0
                else:
                    ob.player_list[ob.position].append(new_card)
        if len(ob.player_list[ob.position]) == 1:
            if ob.easy:
                var=random.randint(0, 1)
                if var:
                    print(var)
                    ob.uno[ob.position] = True
                    ob.message = "%s shouted UNO!" % ob.bot_map[ob.position]
            else:
                ob.uno[ob.position] = True
                ob.message = "%s shouted UNO!" % ob.bot_map[ob.position]
            # ob.message = "%s shouted UNO!" % ob.bot_map[ob.position]  # comment this and uncomment previous
