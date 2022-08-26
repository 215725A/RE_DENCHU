from ast import Nonlocal, Str
from os import access
import secrets
from select import select
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from Model import Model
from Controller import Controller
from SelectImage import SelectImage
 
import re
import random

SM = ScreenManager()
 
####日本語対応用コード
from kivy.core.text import LabelBase, DEFAULT_FONT  # 追加分
from kivy.resources import resource_add_path  # 追加分
resource_add_path('/System/Library/Fonts')  # 追加分
LabelBase.register(DEFAULT_FONT, 'Hiragino Sans GB.ttc')  # 追加分
####日本語対応ここまで

#ウィンドウサイズの定義
Config.set('graphics', 'width', 800)
Config.set('graphics', 'height', 800)
Config.set('graphics', 'resizable', 1)

class StartScene(Screen):
    def __init__(self, **keywargs):
        super().__init__(**keywargs)

    def PressStart(self):
        SM.current = 'select'


class SelectScene(Screen):
    def __init__(self, **keywargs):
        super().__init__(**keywargs)

    def PressBack(self):
        SM.current = 'start'
    
    def PressRed(self):
        SM.current = 'red'

    def PressGreen(self):
        SM.current = 'green'

    def PressYellow(self):
        SM.current = 'yellow'


class DecideRed(Screen):
    def __init__(self, model, controller, selectImage, **keywargs):
        self.controller = controller
        self.model = model
        self.selectImage = selectImage
        super(DecideRed, self).__init__(**keywargs)

    def PressDecide(self):
        self.controller.onPress("denchu_red")
        SM.add_widget(BattleScene(self.model, self.controller, self.selectImage, name='battle'))
        SM.current = 'battle'

    def PressBack(self):
        SM.current = 'select'


class DecideGreen(Screen):
    def __init__(self, model, controller, selectImage, **keywargs):
        self.controller = controller
        self.model = model
        self.selectImage = selectImage
        super(DecideGreen, self).__init__(**keywargs)

    def PressDecide(self):
        self.controller.onPress("denchu_green")
        SM.add_widget(BattleScene(self.model, self.controller, self.selectImage, name='battle'))
        SM.current = 'battle'

    def PressBack(self):
        SM.current = 'select'


class DecideYellow(Screen):
    def __init__(self, model, controller, selectImage, **keywargs):
        self.controller = controller
        self.model = model
        self.selectImage = selectImage
        super(DecideYellow, self).__init__(**keywargs)

    def PressDecide(self):
        self.controller.onPress("denchu_yellow")
        SM.add_widget(BattleScene(self.model, self.controller, self.selectImage, name='battle'))
        SM.current = 'battle'

    def PressBack(self):
        SM.current = 'select'


class BattleScene(Screen):
    def __init__(self, model, controller, selectImage, **keywargs):
        self.controller = controller
        self.model = model
        self.selectImage = selectImage
        self.selectImage.setImage(self.model.opponent.monster.getName(), self.model.player.monster.getName())
        super(BattleScene, self).__init__(**keywargs)

    def getSceneImage(self):
        return self.selectImage.getImage()

    def PressBattle(self):
        SM.add_widget(SkillScene(self.model, self.controller, self.selectImage, name='skill'))
        SM.current = 'skill'

    def PressItem(self):
        if not(self.model.player.monster.getDead() or self.model.opponent.monster.getDead()):
            SM.add_widget(ItemScene(self.model, self.controller, self.selectImage, name='item'))
            SM.current = 'item'
        elif self.model.player.monster.getDead():
            SM.add_widget(LoseScene(self.model, name='lose'))
            SM.current = 'lose'

    def PressEscape(self):
        if not(self.model.player.monster.getDead() or self.model.opponent.monster.getDead()):
            SM.current = 'escape'

    def getDenchuName(self):
        if self.model.player.monster.getName() == "denchu_red" : return "赤色デンチュウ"
        elif self.model.player.monster.getName() == "denchu_green" : return "緑色デンチュウ"
        elif self.model.player.monster.getName() == "denchu_yellow" : return "黄色デンチュウ"

    def getDenchuHP(self):
        return self.model.player.monster.getStrHP()
    
    def getDenchuPower(self):
        return self.model.player.monster.getStrPower()

    def getOpponentName(self):
        if self.model.opponent.monster.getName() == "boss" : return "ボス"
        elif self.model.opponent.monster.getName() == "robot" : return "ロボット"
        elif self.model.opponent.monster.getName() == "enemy" : return "エネミー"

    def getOpponentHP(self):
        return self.model.opponent.monster.getStrHP()

    def getOpponentPower(self):
        return self.model.opponent.monster.getStrPower()


class SkillScene(Screen):
    def __init__(self, model, controller, selectImage, **keywargs):
        self.model = model
        self.controller = controller
        self.executer = self.model.player.monster
        self.selectImage = selectImage
        self.selectImage.setImage(self.model.opponent.monster.getName(), self.model.player.monster.getName())
        self.skillNames = self.model.player.monster.getSkills()
        self.skillName1 = self.skillNames[0].getSkillName()
        self.skillName2 = self.skillNames[1].getSkillName()
        self.skillName3 = self.skillNames[2].getSkillName()
        self.skillName4 = self.skillNames[3].getSkillName()
        super(SkillScene, self).__init__(**keywargs)

    def getSceneImage(self):
        return self.selectImage.getImage()

    def getSkillName1(self):
        return self.skillName1

    def getSkillName2(self):
        return self.skillName2

    def getSkillName3(self):
        return self.skillName3

    def getSkillName4(self):
        return self.skillName4

    def PressBack(self):
        SM.current = 'battle'

    def PressSkill1(self):
        self.controller.PressSkill(self.executer, self.skillName1)
        if not(self.model.player.monster.getDead()) and not(self.model.opponent.monster.getDead()):
            SM.add_widget(EnemyScene(self.model, self.controller, self.selectImage, name='enemy'))
            SM.current = 'enemy'
        elif self.model.opponent.monster.getDead():
            SM.add_widget(WinScene(self.model, name='win'))
            SM.current = 'win'
    
    def PressSkill2(self):
        self.controller.PressSkill(self.executer, self.skillName2)
        if not(self.model.player.monster.getDead()) and not(self.model.opponent.monster.getDead()):
            SM.add_widget(EnemyScene(self.model, self.controller, self.selectImage, name='enemy'))
            SM.current = 'enemy'
        elif self.model.opponent.monster.getDead():
            SM.add_widget(WinScene(self.model, name='win'))
            SM.current = 'win'

    def PressSkill3(self):
        self.controller.PressSkill(self.executer, self.skillName3)
        if not(self.model.player.monster.getDead()) and not(self.model.opponent.monster.getDead()):
            SM.add_widget(EnemyScene(self.model, self.controller, self.selectImage, name='enemy'))
            SM.current = 'enemy'
        elif self.model.opponent.monster.getDead():
            SM.add_widget(WinScene(self.model, name='win'))
            SM.current = 'win'

    def PressSkill4(self):
        self.controller.PressSkill(self.executer, self.skillName4)
        if not(self.model.player.monster.getDead()) and not(self.model.opponent.monster.getDead()):
            SM.add_widget(EnemyScene(self.model, self.controller, self.selectImage, name='enemy'))
            SM.current = 'enemy'
        elif self.model.opponent.monster.getDead():
            SM.add_widget(WinScene(self.model, name='win'))
            SM.current = 'win'


class EnemyScene(Screen):
    def __init__(self, model, controller, selectImage, **keywargs):
        self.model = model
        self.controller = controller
        self.selectImage = selectImage
        self.selectImage.setImage(self.model.opponent.monster.getName(), self.model.player.monster.getName())
        self.executer = self.model.opponent.monster
        self.skills = self.model.opponent.monster.getSkills()
        super(EnemyScene, self).__init__(**keywargs)

    def getSceneImage(self):
        return self.selectImage.getImage()

    def PressBattle(self):
        self.command = random.choice(self.skills)
        self.controller.PressSkill(self.executer, self.command.getSkillName())
        if not(self.model.player.monster.getDead()) and not(self.model.opponent.monster.getDead()):
            SM.add_widget(BattleScene(self.model, self.controller, self.selectImage, name='battle'))
            SM.current = 'battle'
        elif self.model.player.monster.getDead():
            SM.add_widget(LoseScene(self.model, name='lose'))
            SM.current = 'lose'

    def getOpponentName(self):
        if self.model.opponent.monster.getName() == "boss" : return "ボス"
        elif self.model.opponent.monster.getName() == "robot" : return "ロボット"
        elif self.model.opponent.monster.getName() == "enemy" : return "エネミー"


class ItemScene(Screen):
    def __init__(self, model, controller, selectImage, **keywargs):
        self.model = model
        self.controller = controller
        self.selectImage = selectImage
        self.selectImage.setImage(self.model.opponent.monster.getName(), self.model.player.monster.getName())
        self.itemName = self.model.player.items.getItemName()
        self.itemName1 = self.itemName[0]
        self.itemName2 = self.itemName[1]
        super(ItemScene, self).__init__(**keywargs)

    def getSceneImage(self):
        return self.selectImage.getImage()

    def PressItem1(self):
        self.controller.onPress(self.itemName1)
        SM.add_widget(EnemyScene(self.model, self.controller, self.selectImage, name='enemy'))
        SM.current = 'enemy'

    def PressItem2(self):
        self.controller.onPress(self.itemName2)
        SM.add_widget(EnemyScene(self.model, self.controller, self.selectImage, name='enemy'))
        SM.current = 'enemy'

    def getItemName1(self):
        return self.itemName1

    def getItemName2(self):
        return self.itemName2

    def PressBack(self):
        SM.current = 'battle'


class EscapeScene(Screen):
    def __init__(self, **keywargs):
        super(EscapeScene, self).__init__(**keywargs)


class LoseScene(Screen):
    def __init__(self, model, **keywargs):
        self.model = model
        super(LoseScene, self).__init__(**keywargs)
    
    def getDenchuName(self):
        if self.model.player.monster.getName() == "denchu_red" : return "赤色デンチュウ"
        elif self.model.player.monster.getName() == "denchu_green" : return "緑色デンチュウ"
        elif self.model.player.monster.getName() == "denchu_yellow" : return "黄色デンチュウ"


class WinScene(Screen):
    def __init__(self, model, **keywargs):
        self.model = model
        super(WinScene, self).__init__(**keywargs)

    def getOpponentName(self):
        if self.model.opponent.monster.getName() == "boss" : return "ボス"
        elif self.model.opponent.monster.getName() == "robot" : return "ロボット"
        elif self.model.opponent.monster.getName() == "enemy" : return "エネミー"


class DenchuApp(App):
    def __init__(self, **keywargs):
        self.title = 'DENCHU QUEST'
        view = StartScene()
        self.model = Model(view)
        self.model.trainerInit()
        self.controller = Controller(self.model)
        self.selectImage = SelectImage()
        super(DenchuApp, self).__init__(**keywargs)

    def build(self):
        SM.add_widget(StartScene(name='start'))
        SM.add_widget(SelectScene(name='select'))
        SM.add_widget(DecideRed(self.model, self.controller, self.selectImage, name='red'))
        SM.add_widget(DecideGreen(self.model, self.controller, self.selectImage, name='green'))
        SM.add_widget(DecideYellow(self.model, self.controller, self.selectImage, name='yellow'))
        # SM.add_widget(BattleScene(self.model, self.controller, name='battle'))
        # SM.add_widget(SkillScene(self.model, name='skill'))
        # SM.add_widget(ItemScene(self.model, name='item'))
        SM.add_widget(EscapeScene(name='escape'))
        return SM
 
 
if __name__ == '__main__':
   DenchuApp().run()