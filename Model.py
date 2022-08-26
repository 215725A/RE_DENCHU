import random

class Trainer:
    def __init__(self, name):
        self.name = name

    def choseMonster(self, name):
        self.monster.setName(name)
        self.monster.setType()
        self.monster.setSkitlls()

    def fight(self):
        pass


class Player(Trainer):
    def __init__(self):
        self.items = Item()
        self.monster = Monster()
        super().__init__("プレイヤー")

    def useItem(self, command):
        self.items.activateItem(self.monster, command)

    def escape(self):
        pass

class Opponent(Trainer):
    def __init__(self):
        self.names = ["boss", "robot", "enemy"]
        self.monster = Monster()
        super().__init__("コンピュータ")

    def choseMonster(self):
        self.monster = Monster()
        opponentName = random.choice(self.names)
        self.monster.setName(opponentName)
        self.monster.setType()
        self.monster.setSkitlls()



class Item:
    def __init__(self):
        self.itemName = ['おでん', 'バッテリー']
        self.healAmount = 30
        self.addAmount = 5
    
    def activateItem(self, monster, command):
        if command == 'おでん':
            if monster.getHP() == monster.getMAXHP():
                print("回復しても意味ないよ")
            elif (monster.getMAXHP() - monster.getHP()) < self.healAmount:
                print("全回復")
                monster.setHP(monster.getMAXHP())
            elif monster.getHP() > 0:
                print(str(self.healAmount) + "回復した")
                self.amount = monster.getHP() + self.healAmount
                monster.setHP(self.amount)
        elif command == 'バッテリー':
            self.powAmount = monster.getPower() + self.addAmount
            monster.setPower(self.powAmount)

    def getItemName(self):
        return self.itemName


class Monster:
    def __init__(self):
        self.name = "red_denchu"
        self.hp = random.randint(95, 105)
        self.type = "RED"
        self.MAXHP = self.hp
        self.skills = []
        self.power = random.randint(10, 15)
        self.dead = False
        self.damage = 0

    def useSkill(self, exePower, command):
        if command == "普通のパンチ":
            self.attackDamege(exePower, self.skills[0])
        elif command == "マジ殴り":
            self.attackDamege(exePower, self.skills[1])
        elif command in ["きゅうれんぽうとう", "リューイーソー", "チートイ"]:
            self.attackDamege(exePower, self.skills[2])
        elif command in ["ヨガファイヤー", "サンフラワー", "100万ボルト"]:
            self.attackDamege(exePower, self.skills[3])

    def attackDamege(self, exePower, command):
        self.hit = ["hit", "miss"]
        self.weight = [command.getHit(), (1 - command.getHit())]
        self.result = random.choices(self.hit, weights=self.weight, k=1)

        if self.result[0] == "hit":
            print("hit")
            if self.type == "RED" and command.getType() == "YELLOW":
                self.damage = int(exePower * command.getMight() * 2)
            elif self.type == "RED" and command.getType() == "Green":
                self.damage = int(exePower * command.getMight() * 0.5)
            elif self.type == "GREEN" and command.getType() == "RED":
                self.damage = int(exePower * command.getMight() * 2)
            elif self.type == "GREEN" and command.getType() == "YELLOW":
                self.damage = int(exePower * command.getMight() * 0.5)
            elif self.type == "YELLOW" and command.getType() == "Green":
                self.damage = int(exePower * command.getMight() * 2)
            elif self.type == "YELLOW" and command.getType() == "RED":
                self.damage = int(exePower * command.getMight() * 0.5)
            else:
                self.damage = int(exePower * command.getMight())
        else:
            self.damage = 0
            print("miss")

    def recieveDamage(self, exePower, command):
        self.useSkill(exePower, command)
        self.hp -= self.damage
        self.damage = 0
        self.isDead()

    def isDead(self):
        if self.hp <= 0 : self.dead = True
        else : self.dead = False

    def getDead(self):
        return self.dead

    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name

    def setType(self):
        if self.getName() in ["denchu_red", "boss"]:
            self.type = "RED"
        elif self.getName() in ["denchu_green", "robot"]:
            self.type = "GREEN"
        elif self.getName() in ["denchu_yellow", "enemy"]:
            self.type = "YELLOW"

    def getType(self):
        return self.type

    def setSkitlls(self):
        self.skill1 = Skill("普通のパンチ", "WHITE", 1, 1)
        self.skill2 = Skill("マジ殴り", "WHITE", 1.2, 0.8)
        if self.getType() == "RED":
            self.skill3 = Skill("きゅうれんぽうとう", "RED", 1.2, 0.9)
            self.skill4 = Skill("ヨガファイヤー", "RED", 1.5, 0.7)
        elif self.getType() == "GREEN":
            self.skill3 = Skill("リューイーソー", "GREEN", 1.2, 0.9)
            self.skill4 = Skill("サンフラワー", "GREEN", 1.5, 0.7)
        elif self.getType() == "YELLOW":
            self.skill3 = Skill("チートイ", "YELLOW", 1.2, 0.9)
            self.skill4 = Skill("100万ボルト", "YELLOW", 1.5, 0.7)
        
        self.skills = [self.skill1, self.skill2, self.skill3, self.skill4]

    def getSkills(self):
        return self.skills
    
    def getHP(self):
        return self.hp

    def setHP(self, amount):
        self.hp = amount

    def getMAXHP(self):
        return self.MAXHP
    
    def getStrHP(self):
        return str(self.hp)

    def setPower(self, amount):
        self.power = amount

    def getPower(self):
        return self.power

    def getStrPower(self):
        return str(self.power)


class Skill:
    def __init__(self, skName, skType, might, hit):
        self.skillName = skName
        self.skillType = skType
        self.might = might
        self.hit = hit

    def getSkillName(self):
        return self.skillName
    
    def getHit(self):
        return self.hit

    def getMight(self):
        return self.might
    
    def getType(self):
        return self.skillType


class Model:
    def __init__(self, view):
        self.view = view

    def trainerInit(self):
        self.player = Player()
        self.opponent = Opponent()

    def selectMonster(self, name):
        self.player.choseMonster(name)
        self.opponent.choseMonster()
