import pygame
import itertools
import random

pygame.init()  # initializing pygame


class Essentials(object):
    def __init__(self):
        self.p1 = list()
        self.p2 = list()
        self.p3 = list()
        self.p4 = list()
        self.player_list = [self.p1, self.p2, self.p3, self.p4]
        self.deck1 = list()
        self.deck2 = list()
        self.direction_check = 1
        self.position = 0
        self.current = list()
        self.color = ['Blue', 'Red', 'Green', 'Yellow']


class PlayMode(object):
    def __init__(self):
        self.load = "LOAD PAGE"
        self.in_game = "IN GAME"
        self.info = "INFO PAGE"
        self.win = "WINNER"


class Color(object):
    def __init__(self):
        self.black = (0, 0, 0)


class Image(object):
    def __init__(self):
        self.icon = pygame.image.load("./images/icon.png")
        self.load = pygame.image.load("./images/uno_load.png")
        self.bg = pygame.image.load("./images/background.png")
        self.back = pygame.image.load("./images/return-button.png")
        self.mute = pygame.image.load("./images/mute.png")
        self.unmute = pygame.image.load("./images/unmute.png")
        self.p1 = pygame.image.load("./images/woman.png")
        self.p2 = pygame.image.load("./images/man.png")
        self.p3 = pygame.image.load("./images/woman (1).png")
        self.p4 = pygame.image.load("./images/man (1).png")
        self.card_back = pygame.image.load("./images/Back.png")
        self.card_back_l = pygame.image.load("./images/Back_left.png")
        self.card_back_r = pygame.image.load("./images/Back_right.png")
        self.card_back_i = pygame.image.load("./images/Back_inverted.png")
        self.done = pygame.image.load("./images/checked.png")
        self.line = pygame.image.load("./images/minus-line.png")
        self.help = pygame.image.load("./images/help.png")
        self.win = pygame.image.load("./images/winner.png")


class Sound(object):
    def __init__(self):
        self.back_g = "./sound/bg_music.wav"
        self.click = pygame.mixer.Sound('./sound/Minecraft-hat.wav')
        self.card_drawn = pygame.mixer.Sound('./sound/card_drawn.wav')
        self.card_played = pygame.mixer.Sound('./sound/card_played.wav')
        self.shuffled = pygame.mixer.Sound('./sound/shuffle.wav')


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


def get_curr_player(ob):
    if ob.current[0] == 'Reverse':
        ob.direction_check *= -1
    if ob.current[0] == 'Skip' or ob.current[0] == '+4':
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


img = Image()
col = Color()
pm = PlayMode()
sound = Sound()
ess = Essentials()

pygame.mixer.music.load(sound.back_g)
pygame.mixer.music.play(-1)  # continuous bg music
pygame.mixer.music.set_volume(0.05)
music_on = True

root = pygame.display.set_mode((1000, 600))
root.fill(col.black)
pygame.display.set_caption('UNO')
pygame.display.set_icon(img.icon)

active = True
play_mode = pm.load

winner = -1
player_playing = False
play_lag = -1

# Dealing the cards
create(ess)


while active:
    m = pygame.mouse.get_pos()

    for inp in pygame.event.get():
        if inp.type == pygame.QUIT:
            active = False

        if inp.type == pygame.MOUSEBUTTONDOWN:
            # print("x =", m[0], "y =", m[1])
            if 0 < m[0] < 265 and 205 < m[1] < 270 and play_mode == pm.load:
                if music_on:
                    sound.click.play()
                play_mode = pm.in_game
            if 0 < m[0] < 265 and 340 < m[1] < 405 and play_mode == pm.load:
                if music_on:
                    sound.click.play()
                play_mode = pm.info
            if 420 < m[0] < 555 and 425 < m[1] < 543 and play_mode == pm.win:
                if music_on:
                    sound.click.play()
                re_initialize(ess)
                play_mode = pm.load
            if 10 < m[0] < 42 and 10 < m[1] < 42 and (play_mode == pm.in_game or play_mode == pm.info):
                if music_on:
                    sound.click.play()
                play_mode = pm.load
            if 960 < m[0] < 1000 and 0 < m[1] < 40:
                if music_on:
                    sound.click.play()
                if music_on:
                    pygame.mixer.music.pause()
                    music_on = False
                else:
                    pygame.mixer.music.unpause()
                    music_on = True
            if player_playing:
                for i in range(625, 625 - 50 * len(ess.player_list[0]), -50):
                    if i < m[0] < i + 50 and 470 < m[1] < 585:
                        print(int((625 - i) / 50))
                        player_playing = False
                        ess.player_list[0].pop()
                        if music_on:
                            sound.card_played.play()

                if 340 < m[0] < 425 and 240 < m[1] < 355:
                    print("Taken from stack")
                    player_playing = False
                    if music_on:
                        sound.card_drawn.play()

    # HOME PAGE
    if play_mode == pm.load:
        root.blit(img.load, (0, 0))

    # PLAYING MODE
    elif play_mode == pm.in_game:
        if any(map(is_empty, ess.player_list)):
            winner = [ess.player_list.index(x) for x in ess.player_list if len(x) == 0]
            winner = winner[0]
            play_mode = pm.win

        if play_lag == -1 and music_on:
            sound.shuffled.play()

        # Check if anyone has 0 cards if yes then declare winner

        root.blit(img.bg, (0, 0))
        root.blit(img.back, (10, 10))

        for i in range(len(ess.player_list[1])):
            root.blit(img.card_back_l, (40, 335 - 30 * i))
        for i in range(len(ess.player_list[2])):
            root.blit(img.card_back_i, (380 + 30 * i, 20))
        for i in range(len(ess.player_list[3])):
            root.blit(img.card_back_r, (845, 190 + 30 * i))

        for i in range(len(ess.player_list[0])):
            root.blit(pygame.image.load("./images/" + ess.player_list[0][i][1] + str(ess.player_list[0][i][0]) + ".png"), (590 - 50 * i, 470))

        root.blit(img.card_back, (340, 240))
        root.blit(pygame.image.load("./images/" + ess.current[1] + str(ess.current[0]) + ".png"), (580, 240))

        if player_playing:
            root.blit(img.line, (682, 550))
        else:
            if play_lag == 200:
                print("Played: Player #", ess.position)

                if ess.position == 0:
                    print("Player play")
                    player_playing = True
                else:
                    # bot_play(player - 1)
                    ess.player_list[ess.position].pop()
                    pass

                # if player == 0:
                #     current = ("Skip", "Red")
                # else:
                #     current = ("5", "Red")

                get_curr_player(ess)

                if ess.position != 0:
                    play_lag = 0
            else:
                play_lag += 1
                if ess.position == 1:
                    root.blit(img.line, (67, 512))
                elif ess.position == 2:
                    root.blit(img.line, (293, 85))
                elif ess.position == 3:
                    root.blit(img.line, (870, 145))

        root.blit(img.p1, (290, 30))
        root.blit(img.p2, (865, 90))
        root.blit(img.p3, (55, 440))
        root.blit(img.p4, (675, 490))

    # RULES PAGE
    elif play_mode == pm.info:
        root.blit(img.help, (0, 0))
        root.blit(img.back, (10, 10))

    # WIN
    elif play_mode == pm.win:
        string = ""
        if winner == 0:
            string = "Well Done! You've Won this Round!"
        else:
            string = "Bot #%d has won this Round!" % winner

        root.blit(img.win, (0, 0))
        text = pygame.font.Font('Pacifico.ttf', 40).render(string, True, (255, 238, 46))
        text = pygame.transform.rotate(text, 4)
        root.blit(text, [190, 100])

    # EXTRA INTERACTIONS
    if music_on:
        root.blit(img.mute, (960, 8))
    else:
        root.blit(img.unmute, (960, 8))

    # refreshing screen
    pygame.display.update()
