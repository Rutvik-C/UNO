import pygame
from classes import Image, Color, PlayMode, Sound, Essentials
from functions import *


# Initialising Pygame
pygame.init()


# Creating Objects
img = Image()
col = Color()
pm = PlayMode()
sound = Sound()
ess = Essentials()


# Creating root window
root = pygame.display.set_mode((1000, 600))
root.fill(col.black)
pygame.display.set_caption('UNO')
pygame.display.set_icon(img.icon)


# Setting up background Music
pygame.mixer.music.load(sound.back_g)
pygame.mixer.music.play(-1)  # continuous bg music
pygame.mixer.music.set_volume(0.3)
music_on = True


# Setting up initial game variables
active = True
play_mode = pm.load
winner = -1
player_playing = False
play_lag = -1


# Dealing the cards
create(ess)


# Game Loop
while active:

    # Checking for all the occurring events
    for inp in pygame.event.get():

        # Quit button Check
        if inp.type == pygame.QUIT:
            active = False

        # Mouse click Check
        if inp.type == pygame.MOUSEBUTTONDOWN:
            m = pygame.mouse.get_pos()

            if 0 < m[0] < 265 and 205 < m[1] < 270 and play_mode == pm.load:  # Play Button
                if music_on:
                    sound.click.play()
                play_mode = pm.in_game

            if 0 < m[0] < 265 and 340 < m[1] < 405 and play_mode == pm.load:  # Info Button
                if music_on:
                    sound.click.play()
                play_mode = pm.info

            if 10 < m[0] < 42 and 10 < m[1] < 42 and (play_mode == pm.in_game or play_mode == pm.info):  # Back Button
                if music_on:
                    sound.click.play()
                play_mode = pm.load

            if 420 < m[0] < 555 and 425 < m[1] < 543 and play_mode == pm.win:  # Home Button
                if music_on:
                    sound.click.play()
                re_initialize(ess)
                play_mode = pm.load

            if 960 < m[0] < 1000 and 0 < m[1] < 40:  # Music ON OFF Button
                if music_on:
                    sound.click.play()
                if music_on:
                    pygame.mixer.music.pause()
                    music_on = False
                else:
                    pygame.mixer.music.unpause()
                    music_on = True

            if player_playing:  # Card click operations
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

    # HOME PAGE SCREEN
    if play_mode == pm.load:
        root.blit(img.load, (0, 0))

    # PLAYING MODE SCREEN
    elif play_mode == pm.in_game:

        # Checking for winner
        if any(map(is_empty, ess.player_list)):
            winner = [ess.player_list.index(x) for x in ess.player_list if len(x) == 0]
            winner = winner[0]
            play_mode = pm.win

        # Initial dealing sounds
        if play_lag == -1 and music_on:
            sound.shuffled.play()

        # Blitting essential Images
        root.blit(img.bg, (0, 0))
        root.blit(img.back, (10, 10))
        root.blit(img.card_back, (340, 240))
        root.blit(pygame.image.load("./images/" + ess.current[1] + str(ess.current[0]) + ".png"), (580, 240))
        root.blit(img.p1, (290, 30))
        root.blit(img.p2, (865, 90))
        root.blit(img.p3, (55, 440))
        root.blit(img.p4, (675, 490))
        for i in range(len(ess.player_list[1])):
            root.blit(img.card_back_l, (40, 335 - 30 * i))
        for i in range(len(ess.player_list[2])):
            root.blit(img.card_back_i, (380 + 30 * i, 20))
        for i in range(len(ess.player_list[3])):
            root.blit(img.card_back_r, (845, 190 + 30 * i))
        for i in range(len(ess.player_list[0])):
            root.blit(pygame.image.load("./images/" + ess.player_list[0][i][1] + str(ess.player_list[0][i][0]) + ".png"), (590 - 50 * i, 470))

        # Play conditions
        if player_playing:
            root.blit(img.line, (682, 550))

        else:
            if play_lag == 200:  # Lag Implementation
                print("Played: Player #", ess.position)

                # Checking for player played
                if ess.position == 0:
                    print("Player play")
                    player_playing = True
                else:
                    # bot_play(player - 1)
                    ess.player_list[ess.position].pop()
                    pass

                # Calculating next player
                set_curr_player(ess)

                if ess.position != 0:
                    play_lag = 0

            else:
                play_lag += 1

                # Line graphic
                if ess.position == 1:
                    root.blit(img.line, (67, 512))
                elif ess.position == 2:
                    root.blit(img.line, (293, 85))
                elif ess.position == 3:
                    root.blit(img.line, (870, 145))

    # RULES PAGE SCREEN
    elif play_mode == pm.info:
        root.blit(img.help, (0, 0))
        root.blit(img.back, (10, 10))

    # WIN SCREEN
    elif play_mode == pm.win:
        string = ""
        if winner == 0:
            string = "Well Done! You've Won this Round!"
        else:
            string = "Bot #%d has won this Round!" % winner

        # Rendering and blitting
        root.blit(img.win, (0, 0))
        text = pygame.font.Font('Pacifico.ttf', 40).render(string, True, (255, 238, 46))
        text = pygame.transform.rotate(text, 4)
        root.blit(text, [190, 100])

    # Music toggle button
    if music_on:
        root.blit(img.mute, (960, 8))
    else:
        root.blit(img.unmute, (960, 8))

    # Refreshing screen
    pygame.display.update()
