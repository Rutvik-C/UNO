def action():
    global deck1, deck2, current
    global special_check=0
    played_check = 0
    check = 0
    if current[0] == '+2' and special_check == 0:
        for _ in range(2):
            try:
                player_list[position].append(deck1.pop())
            except:
                deck1, deck2 = deck2, deck1
                random.shuffle(deck1)
                player_list[position].append(deck1.pop())
        print("Draw", current[0])
        played_check = 1
        special_check = 1
    if current[0] == '+4' and special_check == 0:
        for _ in range(4):
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
                special_check=0
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
                    special_check=0
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
                    print("\nP", position + 1, " played:",new_card, sep="")
                    new_color = random.choice(color)
                    print("Color changes to:", new_color)
                    current = (new_card[0], new_color)
                    special_check=0
                elif new_card[1] == current[1] or new_card[0]==current[0]:
                    print("\nP", position + 1, " played:",new_card, sep="")
                    deck2.append(new_card)
                    special_check=0
                else:
                    player_list[position].append(new_card)
        if len(player_list[position]) == 1:
            print("UNO!")
