from classes import *
from functions import *

# Initialising Pygame
pygame.init()

# Creating Objects
img = Image()
col = Color()
pm = PlayMode()
sound = Sound()
fnt = TextFont()
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
active = True  # While game is ON this variable is True
play_mode = pm.load
winner = -1
player_playing = False
play_lag = -1

disp = False
win_dec = False
pen_check = False

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

            if ((20 < m[0] < 55 or 210 < m[0] < 245) and 150 < m[1] < 180) and play_mode == pm.load:  # Left Right Button
                if music_on:
                    sound.click.play()
                if ess.easy:
                    ess.easy = False
                else:
                    ess.easy = True

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
                if 850 < m[0] < 916 and 500 < m[1] < 565:  # UNO button
                    if music_on:
                        sound.click.play()
                    ess.uno[0] = True

                if 775 < m[0] < 840 and 505 < m[1] < 570:  # End turn button
                    if music_on:
                        sound.click.play()
                    player_playing = False

                for i in range(625, 625 - 50 * len(ess.player_list[0]), -50):
                    if i < m[0] < i + 50 and 470 < m[1] < 585:
                        play_this_card(ess, ess.player_list[0][int((625 - i) / 50)])
                        if music_on:
                            sound.card_played.play()

                if 340 < m[0] < 425 and 240 < m[1] < 355:
                    take_from_stack(ess)
                    if music_on:
                        sound.card_drawn.play()

            if ess.choose_color:

                if 395 < m[0] < 440 and 390 < m[1] < 450:  # Red Button
                    ess.choose_color = False
                    play_this_card_2(ess, "Red")
                    if music_on:
                        sound.click.play()
                if 450 < m[0] < 495 and 390 < m[1] < 450:  # Green Button
                    ess.choose_color = False
                    play_this_card_2(ess, "Green")
                    if music_on:
                        sound.click.play()
                if 505 < m[0] < 550 and 390 < m[1] < 450:  # Blue Button
                    ess.choose_color = False
                    play_this_card_2(ess, "Blue")
                    if music_on:
                        sound.click.play()
                if 560 < m[0] < 605 and 390 < m[1] < 450:  # Yellow Button
                    ess.choose_color = False
                    play_this_card_2(ess, "Yellow")
                    if music_on:
                        sound.click.play()

    # HOME PAGE SCREEN
    if play_mode == pm.load:
        root.blit(img.load, (0, 0))
        text = pygame.font.Font(fnt.joe_fin, 50).render("<", True, (255, 238, 46))
        root.blit(text, [20, 140])
        text = pygame.font.Font(fnt.joe_fin, 50).render(">", True, (255, 238, 46))
        root.blit(text, [220, 140])
        if ess.easy:
            text = pygame.font.Font(fnt.joe_fin, 30).render("EASY", True, (255, 238, 46))
            root.blit(text, [93, 153])
        else:
            text = pygame.font.Font(fnt.joe_fin, 30).render("HARD", True, (255, 238, 46))
            root.blit(text, [93, 153])

    # PLAYING MODE SCREEN
    elif play_mode == pm.in_game:

        # Checking for winner
        for i in ess.player_list:
            if len(i) == 0:
                win_dec = True
                winner = ess.player_list.index(i)
                break

        # Initial dealing sounds
        if play_lag == -1 and music_on:
            sound.shuffled.play()

        # Blitting essential Images
        root.blit(img.bg, (0, 0))
        root.blit(img.back, (10, 10))
        root.blit(img.card_back, (340, 240))
        try:
            root.blit(pygame.image.load("./images/" + ess.current[1] + str(ess.current[0]) + ".png"), (580, 240))
        except:
            root.blit(pygame.image.load("./images/" + ess.current[1] + ".png"), (580, 240))
        root.blit(img.p1, (290, 30))
        root.blit(img.p2, (865, 90))
        root.blit(img.p3, (55, 440))
        root.blit(img.p4, (675, 490))

        text = pygame.font.Font(fnt.joe_fin, 20).render("YOU", True, (255, 238, 46))
        root.blit(text, [690, 460])
        text = pygame.font.Font(fnt.joe_fin, 20).render("EDITH", True, (255, 238, 46))
        root.blit(text, [295, 4])
        text = pygame.font.Font(fnt.joe_fin, 20).render("JARVIS", True, (255, 238, 46))
        root.blit(text, [870, 60])
        text = pygame.font.Font(fnt.joe_fin, 20).render("FRIDAY", True, (255, 238, 46))
        root.blit(text, [60, 410])

        text = pygame.font.Font(fnt.joe_fin, 20).render(ess.message, True, (255, 238, 46))
        root.blit(text, [340, 210])

        for i in range(len(ess.player_list[1])):
            root.blit(img.card_back_l, (40, 315 - 30 * i))
        for i in range(len(ess.player_list[2])):
            root.blit(img.card_back_i, (380 + 30 * i, 20))
        for i in range(len(ess.player_list[3])):
            root.blit(img.card_back_r, (845, 190 + 30 * i))
        for i in range(len(ess.player_list[0])):
            root.blit(
                pygame.image.load("./images/" + ess.player_list[0][i][1] + str(ess.player_list[0][i][0]) + ".png"),
                (590 - 50 * i, 470))

        if ess.choose_color:
            root.blit(img.red, (395, 390))
            root.blit(img.green, (450, 390))
            root.blit(img.blue, (505, 390))
            root.blit(img.yellow, (560, 390))

        # Play conditions
        if player_playing:
            ess.message = ""

            if not ess.drawn and not ess.played:
                if ess.current[0] == '+2' and ess.special_check == 0:
                    for _ in range(2):
                        try:
                            ess.player_list[0].append(ess.deck1.pop())
                        except:
                            ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                            random.shuffle(ess.deck1)
                            ess.player_list[0].append(ess.deck1.pop())
                    print("Draw", ess.current[0])
                    ess.special_check = 1
                    player_playing = False
                elif ess.current[0] == '+4' and ess.special_check == 0:
                    for _ in range(4):
                        try:
                            ess.player_list[0].append(ess.deck1.pop())
                        except:
                            ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                            random.shuffle(ess.deck1)
                            ess.player_list[0].append(ess.deck1.pop())
                    ess.special_check = 1
                    player_playing = False

            root.blit(img.line, (682, 550))
            root.blit(img.done, (775, 505))
            root.blit(img.uno_button, (850, 500))

        else:
            if play_lag == 200:  # Lag Implementation
                disp = False
                pen_check = False

                # Calculating next player
                set_curr_player(ess, True)
                print("calling bot fun ->", ess.position)

                # Checking for player played
                if ess.position == 0:
                    print("Player play")
                    ess.uno[0] = False
                    player_playing = True

                else:
                    # Reinitialising Flags
                    ess.played = False
                    ess.drawn = False

                    bot_action(ess)

                print()

                # for i in ess.player_list:

                # if (ess.direction_check == 1 and ess.position != 3) or (ess.direction_check == -1 and ess.position != 1):
                play_lag = 0

            else:
                if win_dec and play_lag == 100:
                    play_mode = pm.win

                if not pen_check:
                    print("Pre penalty:", ess.position, ess.player_list[ess.position], ess.uno[ess.position])
                    if ess.position != -1 and len(ess.player_list[ess.position]) == 1 and not ess.uno[
                       ess.position]:  # Penalty
                        print("PENALTY TO", ess.position, "\nBefore", ess.player_list[0], "\n",
                              ess.player_list[1], "\n", ess.player_list[2], "\n", ess.player_list[3])
                        for j in range(4):
                            if ess.position != j:
                                ess.player_list[ess.position].append(ess.player_list[j].pop())

                        ess.message = "Penalty!"
                        ess.uno[ess.position] = True
                        print("After", ess.player_list[0], "\n", ess.player_list[1], "\n", ess.player_list[2], "\n",
                              ess.player_list[3])
                    pen_check = True

                play_lag += 1

                if not disp:
                    print("\n*** %d ***\n*** gen=%d ***\n" % (ess.position, (ess.position + ess.direction_check) % 4))
                    disp = True

                # Line graphic
                if (ess.position + ess.direction_check) % 4 == 1:
                    root.blit(img.line, (67, 512))
                elif (ess.position + ess.direction_check) % 4 == 2:
                    root.blit(img.line, (293, 85))
                elif (ess.position + ess.direction_check) % 4 == 3:
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
            string = "%s has won this Round" % ess.bot_map[winner]

        # Rendering and blitting
        root.blit(img.win, (0, 0))
        text = pygame.font.Font(fnt.pacifico, 40).render(string, True, (255, 238, 46))
        # text = pygame.transform.rotate(text, 4)
        root.blit(text, [190, 100])

    # Music toggle button
    if music_on:
        root.blit(img.mute, (960, 8))
    else:
        root.blit(img.unmute, (960, 8))

    # Refreshing screen
    pygame.display.update()
