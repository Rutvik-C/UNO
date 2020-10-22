import pygame


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
        self.position = -1
        self.current = list()
        self.drawn = False
        self.played = False
        self.choose_color = False
        self.played_check = 0
        self.special_check = 0
        self.uno = False
        self.message = "DEALING THE CARDS"
        self.bot_map = {1: "FRIDAY", 2: "EDITH", 3: "JARVIS"}
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
        self.pick_color = pygame.image.load("./images/microsoft.png")
        self.uno = pygame.image.load("./images/UNO.png")
        self.uno_button = pygame.image.load("./images/UNOButton.png")


class Sound(object):
    def __init__(self):
        self.back_g = "./sound/bg_music.wav"
        self.click = pygame.mixer.Sound('./sound/Minecraft-hat.wav')
        self.card_drawn = pygame.mixer.Sound('./sound/card_drawn.wav')
        self.card_played = pygame.mixer.Sound('./sound/card_played.wav')
        self.shuffled = pygame.mixer.Sound('./sound/shuffle.wav')


class TextFont(object):
    def __init__(self):
        self.pacifico = "./fonts/Pacifico.ttf"
        self.joe_fin = "./fonts/JosefinSans-Bold.ttf"
