'''
карта 10x10
@ - игрок
^ - гора (камень 70%, железо 30%)                                   +
- - равнина (дерево 50%, хлеб 50%)                                  +
~ - моря                                                            +
= - мост через воду (5 дерева и 3 камня)                            +
A - лагерь (10 дерева и 5 камня)                                    +
# - город (в лагере прожать r, 20 камня, 20 дерева и 10 железа)
при добыче ресурсов х% что потратиться хлеб                         +
'''

import random
import os

playerline = 6
playercoln = 4

size = 10
field = list()
symbols = ["^", "-", "~"]

askedhint = False

bread = 100
wood = 100
stone = 100
iron = 100

campmoun = 0
campplain = 0

actioncount = 0

def makemap():
    global field
    field.clear()
    for i in range(size):
        field.append(list())
    for i in range(size):
        for n in range(size):
            field[i].append(random.choice(symbols))

def startgame():
    makemap()
    while field[playerline][playercoln] == "~":
        makemap()

def drawmap():
    os.system('cls' if os.name == 'nt' else 'clear')

    if askedhint:
        print("w, a, s, d - движение")
        print("e - собрать ресурсы")
        print("r - разбить лагерь, улучшить до города")
        print("t - сохранить игру")
        print("g - загрузить сохранение")
        print("qw/qa/qs/qd - построить мост")
    else:
        print("H - подсказки")

    for line in range(size):
        for elem in range(size):
            if line == playerline and elem == playercoln:
                print("@  ", end = '')
            else:
                print(field[line][elem], ' ', end = '')
        print()

    print(f"Ландшафт: {field[playerline][playercoln]}")
    print(f"Д: {wood}, Ж: {iron}, Х: {bread}, К: {stone}")

def action():
    result = True
    global playerline, playercoln, askedhint
    askedhint = False
    cmd = input("Введите команду: ")
    cmd = cmd.lower()
    if cmd in ["w", "a", "s", "d"]:
        result = move(cmd)
    if cmd == "h":
        hint()
    if cmd == "e":
        inter(cmd)
    if cmd == "r":
        result = camp()
    if cmd in ["qw", "qa", "qs", "qd"]:
        result = bridge(cmd)
    if result == True:
        counter()
    if cmd == "t":
        save()
    if cmd == "g":
        load()
    

def move(cmd):
    global playerline, playercoln, bread
    playerlinelast = playerline
    playercolnlast = playercoln
    if cmd == "w":
            playerline -= 1
    elif cmd == "s":
            playerline += 1
    elif cmd == "a":
            playercoln -= 1
    elif cmd == "d":
            playercoln += 1

    #здесь мы корректируем положение игрока, если он вышел за край карты
    if playerline < 0:
        playerline = 0
    if playerline > size - 1:
        playerline = size - 1
    if playercoln < 0:
        playercoln = 0
    if playercoln > size - 1:
        playercoln = size - 1
    if field[playerline][playercoln] == "~":
        playerline = playerlinelast
        playercoln = playercolnlast
    if playerline != playerlinelast or playercoln != playercolnlast:
        eat()
        return True
    else:
        return False

def hint():
    global askedhint
    askedhint = True

def inter(cmd):
    global wood, bread, stone, iron
    plain = "ДХ"
    mountains = "КККККККЖЖЖ"
    if cmd == 'e':
        if field[playerline][playercoln] == "-":
            res = random.choice(plain)
            if res == "Д":
                wood += 1
            elif res == "Х":
                bread += 1
        elif field[playerline][playercoln] == "^":
            res = random.choice(mountains)
            if res == "Ж":
                iron += 1
            elif res == "К":
                stone += 1
        eat()
    elif cmd == 'campmoun':
        res = random.choice(mountains)
        if res == "Ж":
            iron += 1
        elif res == "К":
            stone += 1
    elif cmd == 'campplain':
        res = random.choice(plain)
        if res == "Д":
            wood += 1
        elif res == "Х":
            bread += 1

        

def camp():
    global wood, stone, iron, field, campmoun, campplain
    
    if wood >= 20 and stone >= 20 and iron >= 10 and field[playerline][playercoln] in ["А", "A"]:
        wood -= 20
        stone -= 20
        iron -= 10
        if field[playerline][playercoln] == "А":
            field[playerline][playercoln] = "#"
            campmoun += 1
            return True
        if field[playerline][playercoln] == "A":
            field[playerline][playercoln] = "#"
            campplain += 1
            return True
    
    if stone >= 5 and wood >= 10 and field[playerline][playercoln] != "=":
        stone -= 5
        wood -= 10
        if field[playerline][playercoln] == "^":
            field[playerline][playercoln] = "А"
            campmoun += 1
            return True
        if field[playerline][playercoln] == "-":
            field[playerline][playercoln] = "A"
            campplain += 1
            return True
    
    return False
            

def eat():
    global bread
    chance = "------===="
    ch = random.choice(chance)
    if ch == "-":
        bread -= 1
    if bread < 0:
        exit()
    

def counter():
    global actioncount 
    actioncount += 1
    if actioncount == 3:
        for i in range(campplain):
            inter('campplain')
        for n in range(campmoun):
            inter('campmoun')
        actioncount = 0

def bridge(cmd):
    global playerline, playercoln, field, wood, stone
    if wood < 5 or stone < 3: return
    
    if cmd == "qw" and field[playerline - 1][playercoln] == "~":
        field[playerline - 1][playercoln] = "="
        wood -= 5
        stone -= 3
        eat()

    if cmd == "qs" and field[playerline + 1][playercoln] == "~":
        field[playerline + 1][playercoln] = "="
        wood -= 5
        stone -= 3
        eat()

    if cmd == "qa" and field[playerline][playercoln - 1] == "~":
        field[playerline ][playercoln - 1] = "="
        wood -= 5
        stone -= 3
        eat()
        
        
    if cmd == "qd" and field[playerline][playercoln + 1] == "~":
        field[playerline][playercoln + 1] = "="
        wood -= 5
        stone -= 3
        eat()

def save():
    with open("file.txt", "w") as f:
        f.write(f"wood {wood}\n")
        f.write(f"stone {stone}\n")
        f.write(f"iron {iron}\n")
        f.write(f"bread {bread}\n")
        f.write(f"actioncount {actioncount}\n")
        f.write(f"campplain {campplain}\n")
        f.write(f"campmoun {campmoun}\n")
        f.write(f"playerline {playerline}\n")
        f.write(f"playercoln {playercoln}\n")
        f.write("field ")
        for i in field:
            for n in i:
                f.write(n)

def load():
    global wood, stone, iron, bread, actioncount, campplain, campmoun, field, playercoln, playerline
    with open("file.txt") as file:
        data = file.readlines()
        for line in data:
            line1 = line.split()
            name = line1[0]
            value = line1[1]
            if name == "wood":
                wood = int(value)
            elif name == "stone":
                stone = int(value)
            elif name == "iron":
                iron = int(value)
            elif name == "bread":
                bread = int(value)
            elif name == "actioncount":
                actioncount = int(value)
            elif name == "campplain":
                campplain = int(value)
            elif name == "campmoun":
                campmoun = int(value)
            elif name == "playercoln":
                playercoln = int(value)
            elif name == "playerline":
                playerline = int(value)
            elif name == "field":
                field.clear()
                for i in range(size):
                    field.append(list())
                for i in range(size):
                    for n in range(size):
                        field[i].append(value[n + size * i])
            
startgame()
drawmap()

while True:
    action()
    drawmap()
