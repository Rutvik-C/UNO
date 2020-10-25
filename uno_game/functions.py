import itertools
import random


def peek(s):
    """Peek"""
    return s[-1]


def create(ob):
    """Dealing the cards"""
    a = ('0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9',
         '+2', '+2', 'Skip', 'Skip', 'Reverse', 'Reverse')
    ob.deck1 = list(itertools.product(a, ob.color))  # Deck created
    for _ in range(4):  # Adds special black cards to decks
        ob.deck1.append(('Wild', 'Black'))
        ob.deck1.append(('+4', 'Black'))
    random.shuffle(ob.deck1)  # Shuffles deck

    while peek(ob.deck1) in [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Skip', 'Green'),
                             ('Skip', 'Blue'), ('Skip', 'Yellow'), ('Reverse', 'Red'), ('Reverse', 'Green'),
                             ('Reverse', 'Blue'), ('Reverse', 'Yellow'), ('+2', 'Red'), ('+2', 'Green'),
                             ('+2', 'Blue'), ('+2', 'Yellow')]:  # First card cannot be special card
        random.shuffle(ob.deck1)

    ob.deck2.append(ob.deck1.pop())  # Shifts first card to played deck
    ob.current = peek(ob.deck2)  # Peek from played deck

    for j in range(4):  # Deals cards to player
        for _ in range(7):
            ob.player_list[j].append(ob.deck1.pop())

    # ob.player_list[0] = [('Wild', 'Black'), ('+4', 'Black'), ('Skip', 'Red'), ('Reverse', 'Green'), ("+2", "Blue")]


def set_curr_player(ob, default):
    """Decides next player"""
    if ob.current[0] == 'Reverse' and ob.special_check == 0:
        ob.direction_check *= -1  # Direction reversed
        ob.special_check = 1  # Special card status inactive
    if ob.current[0] == 'Skip' and ob.special_check == 0:
        ob.special_check = 1
        ob.position = (ob.position + ob.direction_check) % 4

    if default:
        ob.position = (ob.position + ob.direction_check) % 4


def re_initialize(ob):
    """Reinitialize all the game variables and flags"""
    ob.message = ""  # To print message
    ob.winner = -1
    ob.player_playing = False
    ob.play_lag = -1
    ob.player_list = [[], [], [], []]
    ob.deck1 = list()
    ob.deck2 = list()
    ob.direction_check = 1  # Flag to check direction of play
    ob.position = -1  # Position counter
    ob.special_check = 0  # Flag to check status of special card
    ob.current = tuple()
    ob.drawn, ob.played, ob.choose_color = False, False, False
    ob.uno = [True] * 4
    ob.easy = True

    # Dealing the cards
    create(ob)


def take_from_stack(ob):
    """Draw card from stack by user"""
    if not ob.drawn:
        try:
            ob.player_list[0].append(ob.deck1.pop())
        except:
            ob.deck1, ob.deck2 = ob.deck2, ob.deck1
            random.shuffle(ob.deck1)
            ob.player_list[0].append(ob.deck1.pop())
        finally:
            ob.drawn = True


def play_this_card(ob, card):
    """Play card by user"""
    if not ob.played:
        if card[0] == ob.current[0] or card[1] == ob.current[1]:
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
            ob.deck2.append(card)


def play_this_card_2(ob, color):
    """Post color selection"""
    ob.deck2[-1] = (ob.deck2[-1][0], color)
    ob.current = peek(ob.deck2)
    ob.special_check = 0


def handle24(ob, n):
    """Handles +2 and +4 cards"""
    for _ in range(n):
        try:
            ob.player_list[ob.position].append(ob.deck1.pop())
        except:
            ob.deck1, ob.deck2 = ob.deck2, ob.deck1
            random.shuffle(ob.deck1)
            ob.player_list[ob.position].append(ob.deck1.pop())
    ob.message = "%s Draws %d cards" % (ob.bot_map[ob.position], n)
    ob.special_check = 1


def handle_black(ob, item):
    """Handles black cards"""
    ob.special_check = 0
    ob.deck2.append(item)
    ob.current = peek(ob.deck2)
    if not ob.easy:  # Color picker for hard mode
        d = dict()
        d['Blue'] = 0
        d['Green'] = 0
        d['Yellow'] = 0
        d['Red'] = 0
        d['Black'] = 0
        for _item in ob.player_list[ob.position]:
            d[_item[1]] += 1
        d = sorted(d.items(), key=lambda kv: (kv[1], kv[0]))
        new_color = d[-1][0]  # Picks  most frequent color
        if new_color == 'Black':
            new_color = d[-2][0]
    else:
        new_color = random.choice(ob.color)  # Random color picked for easy mode
    ob.message = "%s plays %s %s, new color is %s" % (ob.bot_map[ob.position], item[0], item[1], new_color)
    ob.current = (ob.current[0], new_color)


def bot_play_card(ob, item):
    """Bot plays a card"""
    ob.special_check = 0
    ob.deck2.append(item)
    ob.current = peek(ob.deck2)
    ob.message = "%s plays card %s" % (ob.bot_map[ob.position], ob.current[1] + " " + ob.current[0])


def bot_action(ob, sounds):
    """Bot logic"""
    ob.message = ""
    ob.uno[ob.position] = False
    ob.check = 0
    if (ob.current[0] == '+2' or ob.current[0] == '+4') and ob.special_check == 0:
        handle24(ob, int(ob.current[0][1]))
        ob.played_check = 1

    else:
        check = 0
        for item in ob.player_list[ob.position]:
            if ob.current[1] in item or ob.current[0] in item:
                bot_play_card(ob, item)

                if item[1] == 'Black':
                    handle_black(ob, item)

                ob.player_list[ob.position].remove(item)

                set_curr_player(ob, False)
                check = 1
                break

        if check == 0:
            black_check = 0
            for item in ob.player_list[ob.position]:
                if 'Black' in item:
                    ob.message = "%s plays %s" % (ob.bot_map[ob.position], item[0] + " " + item[1])
                    handle_black(ob, item)
                    ob.player_list[ob.position].remove(item)
                    black_check = 1
                    break
            if black_check == 0:
                try:
                    new_card = (ob.deck1.pop())
                except:
                    ob.deck1, ob.deck2 = ob.deck2, ob.deck1
                    random.shuffle(ob.deck1)
                    new_card = (ob.deck1.pop())

                ob.message = "%s draws a card" % ob.bot_map[ob.position]

                if new_card[1] == 'Black':
                    ob.message = "%s plays %s" % (ob.bot_map[ob.position], new_card[0] + " " + new_card[1])
                    handle_black(ob, new_card)
                elif new_card[1] == ob.current[1] or new_card[0] == ob.current[0]:
                    bot_play_card(ob, new_card)
                else:
                    ob.player_list[ob.position].append(new_card)
        if len(ob.player_list[ob.position]) == 1:
            if ob.easy and random.randint(0, 1):
                ob.uno[ob.position] = True
                ob.message = "%s shouted UNO!" % ob.bot_map[ob.position]
                sounds.uno.play()
            else:
                ob.uno[ob.position] = True
                ob.message = "%s shouted UNO!" % ob.bot_map[ob.position]
                sounds.uno.play()
