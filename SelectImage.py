class SelectImage:
    #デンチュウの色と相手モンスターの組み合わせによって表示する画像を決める
    def __init__(self):
        self.image = './images/red_boss.png'

    def setImage(self,opponentName,denchuName):
        if opponentName == 'boss' and denchuName == 'denchu_red':
            self.image = './images/red_boss.png'
        elif opponentName == 'enemy' and denchuName == 'denchu_red':
            self.image = './images/red_enemy.png'
        elif opponentName == 'robot' and denchuName == 'denchu_red':
            self.image = './images/red_robot.png'
        elif opponentName == 'boss' and denchuName == 'denchu_yellow':
            self.image = './images/yellow_boss.png'
        elif opponentName == 'enemy' and denchuName == 'denchu_yellow':
            self.image = './images/yellow_enemy.png'
        elif opponentName == 'robot' and denchuName == 'denchu_yellow':
            self.image = './images/yellow_robot.png'
        elif opponentName == 'boss' and denchuName == 'denchu_green':
            self.image = './images/green_boss.png'
        elif opponentName == 'enemy' and denchuName == 'denchu_green':
            self.image = './images/green_enemy.png'
        elif opponentName == 'robot' and denchuName == 'denchu_green':
            self.image = './images/green_robot.png'
        else:
            self.image = 'none.png'

    def getImage(self):
        return self.image