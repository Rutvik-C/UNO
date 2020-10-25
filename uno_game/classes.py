import pygame


class Essentials(object):
    def __init__(self):
        self.player_list = [[], [], [], []]  # Generalised ll -> For storing players' cards
        self.deck1 = list()
        self.deck2 = list()
        self.direction_check = 1  # Tracking direction of game
        self.position = -1  # Playing player index
        self.current = list()  # Current card on top of stack

        self.drawn = False  # User play flags
        self.played = False
        self.choose_color = False
        self.player_playing = False
        self.winner = -1
        self.play_lag = -1
        self.play_mode = ""

        self.played_check = 0  # Play checker
        self.special_check = 0  # Special card overhead checker
        self.uno = [True] * 4  # UNO shout flags
        self.message = "DEALING THE CARDS"  # In game messages
        self.easy = True  # Difficulty level
        self.bot_map = {1: "FRIDAY", 2: "EDITH", 3: "JARVIS"}  # Indexing bot index to name
        self.color = ['Blue', 'Red', 'Green', 'Yellow']  # Colors


class PlayMode(object):
    def __init__(self):
        # Declaring various playing modes
        self.load = "LOAD PAGE"
        self.in_game = "IN GAME"
        self.info = "INFO PAGE"
        self.win = "WINNER"


class Image(object):
    def __init__(self):
        # Loading required image files
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
        self.red = pygame.image.load("./images/SmallRed.png")
        self.blue = pygame.image.load("./images/SmallBlue.png")
        self.yellow = pygame.image.load("./images/SmallYellow.png")
        self.green = pygame.image.load("./images/SmallGreen.png")


class Sound(object):
    def __init__(self):
        # Loading required sound files
        self.back_g = "./sound/bg.wav"
        self.click = pygame.mixer.Sound('./sound/Minecraft-hat.wav')
        self.card_drawn = pygame.mixer.Sound('./sound/card_drawn.wav')
        self.card_played = pygame.mixer.Sound('./sound/card_played.wav')
        self.shuffled = pygame.mixer.Sound('./sound/shuffle.wav')
        self.uno = pygame.mixer.Sound("./sound/Recording.wav")
        self.victory = pygame.mixer.Sound("./sound/victory.wav")


class TextFont(object):
    def __init__(self):
        # Loading required font files
        self.pacifico = "./fonts/Pacifico.ttf"
        self.joe_fin = "./fonts/JosefinSans-Bold.ttf"
