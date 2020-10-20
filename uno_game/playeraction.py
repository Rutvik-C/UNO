def playeraction(card):
    if card[0]==current[0] or card[1]==current[1]:
        print("P1 played",card)
        deck2.append(card)
        current=peek(deck2)
        p1.remove(current)
        special_check=0
        return True
    if card[1]=='Black':
        newcolor=input()
        print("new color is:",newcolor)
        p1.remove(card)
        card=(card[0],newcolor)
        deck2.append(card)
        current=peek(deck2)
        special_check=0
        return True
    return False
