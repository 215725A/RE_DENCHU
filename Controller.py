class Controller:
    def __init__(self, model):
        self.model = model
        self.skillSelects = ['普通のパンチ', 'マジ殴り', 'きゅうれんぽうとう', 'ヨガファイヤー', 'リューイーソー', 'サンフラワー', 'チートイ', '100万ボルト']
        self.denchus = ['denchu_red', 'denchu_green', 'denchu_yellow']
        self.opponents = ['boss', 'robot', 'enemy']
        self.items = ['おでん', 'バッテリー']

    def onPress(self, command):
        if command in 'denchu_red':
            self.model.selectMonster(command)
        elif command in 'denchu_green':
            self.model.selectMonster(command)
        elif command in 'denchu_yellow':
            self.model.selectMonster(command)
        elif command in self.items:
            self.model.player.useItem(command)
    
    def PressSkill(self, executer, command):
        if command in self.skillSelects and executer.getName() in self.denchus:
            self.model.opponent.monster.recieveDamage(executer.getPower(), command)
        elif command in self.skillSelects and executer.getName() in self.opponents:
            self.model.player.monster.recieveDamage(executer.getPower(), command)