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

    while peek(ob.deck1) in [('Wild', 'Black'), ('+4', 'Black')]:
        random.shuffle(ob.deck1)

    ob.deck2.append(ob.deck1.pop())
    ob.current = ob.deck2[-1]

    for j in range(4):
        for _ in range(7):
            ob.player_list[j].append(ob.deck1.pop())


def set_curr_player(ob):
    if ob.current[0] == 'Reverse':
        ob.direction_check *= -1
    if ob.current[0] == 'Skip':
        ob.position = (ob.position + ob.direction_check) % 4
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
    ob.position = 0
    ob.current = list()

    # Dealing the cards
    create(ob)


def take_from_stack(ob):
    if not ob.taken_from_stack:
        ob.player_list[0].append(ob.deck1.pop())
        ob.taken_from_stack = True

