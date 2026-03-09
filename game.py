import random
import os


class Player:
    def __init__(self):
        self.line = random.randint(1, 10)
        self.coln = 4
        self.bread = 100
        self.wood = 100
        self.stone = 100
        self.iron = 100
        self.actioncount = 0
        self.campplain = 0
        self.campmoun = 0
        self.askedhint = False

    def eat(self):
        chance = "------===="
        ch = random.choice(chance)
        if ch == "-":
            self.bread -= 1
        if self.bread < 0:
            exit()

    def counter(self, field):
        self.actioncount += 1
        if self.actioncount == 3:
            for i in range(self.campplain):
                self.inter('campplain', field)
            for n in range(self.campmoun):
                self.inter('campmoun', field)
            self.actioncount = 0

    def action(self, field):
        result = True
        self.askedhint = False
        cmd = input("Введите команду: ")
        cmd = cmd.lower()
        if cmd in ["w", "a", "s", "d"]:
            result = self.move(cmd, field)
        if cmd == "h":
            self.hint()
        if cmd == "e":
            self.inter(cmd, field)
        if cmd == "r":
            result = self.camp(field)
        if cmd in ["qw", "qa", "qs", "qd"]:
            result = self.bridge(cmd, field)
        if result == True:
            self.counter(field)
        if cmd == "t":
            self.save(field)
        if cmd == "g":
            self.load(field)

    def move(self, cmd, field):
        playerlinelast = self.line
        playercolnlast = self.coln
        if cmd == "w":
                self.line -= 1
        elif cmd == "s":
                self.line += 1
        elif cmd == "a":
                self.coln -= 1
        elif cmd == "d":
                self.coln += 1

        #здесь мы корректируем положение игрока, если он вышел за край карты
        if self.line < 0:
            self.line = 0
        if self.line > field.size - 1:
            self.line = field.size - 1
        if self.coln < 0:
            self.coln = 0
        if self.coln > field.size - 1:
            self.coln = field.size - 1
        if field.field[self.line][self.coln] == "~":
            self.line = playerlinelast
            self.coln = playercolnlast
        if self.line != playerlinelast or self.coln != playercolnlast:
            self.eat()
            return True
        else:
            return False
        
    def hint(self):
        self.askedhint = True

    def inter(self, cmd, field):
        plain = "ДХ"
        mountains = "КККККККЖЖЖ"
        if cmd == 'e':
            if field.field[self.line][self.coln] == "-":
                res = random.choice(plain)
                if res == "Д":
                    self.wood += 1
                elif res == "Х":
                    self.bread += 1
            elif field.field[self.line][self.coln] == "^":
                res = random.choice(mountains)
                if res == "Ж":
                    self.iron += 1
                elif res == "К":
                    self.stone += 1
            self.eat()
        elif cmd == 'campmoun':
            res = random.choice(mountains)
            if res == "Ж":
                self.iron += 1
            elif res == "К":
                self.stone += 1
        elif cmd == 'campplain':
            res = random.choice(plain)
            if res == "Д":
                self.wood += 1
            elif res == "Х":
                self.bread += 1

    def camp(self, field):
        if self.wood >= 20 and self.stone >= 20 and self.iron >= 10 and field.field[self.line][self.coln] in ["А", "A"]:
            self.wood -= 20
            self.stone -= 20
            self.iron -= 10
            if field.field[self.line][self.coln] == "А":
                field.field[self.line][self.coln] = "#"
                self.campmoun += 1
                return True
            if field.field[self.line][self.coln] == "A":
                field.field[self.line][self.coln] = "#"
                self.campplain += 1
                return True
        
        if self.stone >= 5 and self.wood >= 10 and field.field[self.line][self.coln] != "=":
            self.stone -= 5
            self.wood -= 10
            if field.field[self.line][self.coln] == "^":
                field.field[self.line][self.coln] = "А"
                self.campmoun += 1
                return True
            if field.field[self.line][self.coln] == "-":
                field.field[self.line][self.coln] = "A"
                self.campplain += 1
                return True
        
        return False
    
    def bridge(self, cmd, field):
        if self.wood < 5 or self.stone < 3: return
        
        if cmd == "qw" and field.field[self.line - 1][self.coln] == "~":
            field.field[self.line - 1][self.coln] = "="
            self.wood -= 5
            self.stone -= 3
            self.eat()

        if cmd == "qs" and field.field[self.line + 1][self.coln] == "~":
            field.field[self.line + 1][self.coln] = "="
            self.wood -= 5
            self.stone -= 3
            self.eat()

        if cmd == "qa" and field.field[self.line][self.coln - 1] == "~":
            field.field[self.line ][self.coln - 1] = "="
            self.wood -= 5
            self.stone -= 3
            self.eat()
            
            
        if cmd == "qd" and field.field[self.line][self.coln + 1] == "~":
            field.field[self.line][self.coln + 1] = "="
            self.wood -= 5
            self.stone -= 3
            self.eat()

    def save(self, field):
        with open("file.txt", "w") as f:
            f.write(f"wood {self.wood}\n")
            f.write(f"stone {self.stone}\n")
            f.write(f"iron {self.iron}\n")
            f.write(f"bread {self.bread}\n")
            f.write(f"actioncount {self.actioncount}\n")
            f.write(f"campplain {self.campplain}\n")
            f.write(f"campmoun {self.campmoun}\n")
            f.write(f"playerline {self.line}\n")
            f.write(f"playercoln {self.coln}\n")
            f.write("field ")
            for i in field.field:
                for n in i:
                    f.write(n)

    def load(self, field):
        with open("file.txt") as file:
            data = file.readlines()
            for line in data:
                line1 = line.split()
                name = line1[0]
                value = line1[1]
                if name == "wood":
                    self.wood = int(value)
                elif name == "stone":
                    self.stone = int(value)
                elif name == "iron":
                    self.iron = int(value)
                elif name == "bread":
                    self.bread = int(value)
                elif name == "actioncount":
                    self.actioncount = int(value)
                elif name == "campplain":
                    self.campplain = int(value)
                elif name == "campmoun":
                    self.campmoun = int(value)
                elif name == "playercoln":
                    self.coln = int(value)
                elif name == "playerline":
                    self.line = int(value)
                elif name == "field":
                    field.field.clear()
                    for i in range(field.size):
                        field.field.append(list())
                    for i in range(field.size):
                        for n in range(field.size):
                            field.field[i].append(value[n + field.size * i])

class Field:
    def __init__(self):
        self.size = 10
        self.field = list()
        self.symbols = ["^", "-", "~"]
    def makemap(self):
        self.field.clear()
        for i in range(self.size):
            self.field.append(list())
        for i in range(self.size):
            for n in range(self.size):
                self.field[i].append(random.choice(self.symbols))
    def drawmap(self, player):
        os.system('cls' if os.name == 'nt' else 'clear')

        if player.askedhint:
            print("w, a, s, d - движение")
            print("e - собрать ресурсы")
            print("r - разбить лагерь, улучшить до города")
            print("t - сохранить игру")
            print("g - загрузить сохранение")
            print("qw/qa/qs/qd - построить мост")
        else:
            print("H - подсказки")

        for line in range(self.size):
            for elem in range(self.size):
                if line == player.line and elem == player.coln:
                    print("@  ", end = '')
                else:
                    print(self.field[line][elem], ' ', end = '')
            print()

        print(f"Ландшафт: {self.field[player.line][player.coln]}")
        print(f"Д: {player.wood}, Ж: {player.iron}, Х: {player.bread}, К: {player.stone}")



f = Field()
f.makemap()
p1 = Player()
f.drawmap(p1)

while True:
    p1.action(f)
    f.drawmap(p1)
