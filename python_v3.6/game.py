import pygame

from world import World
from message import Message, Button

import levels


class STATE:
    INITIAL = 0
    CHOOSE_POWER = 1
    WAIT_UNTILL_STOP = 10
    PAUSE = 15
    WIN = 100
    LOSS = 20


class Game:
    LEVELS = [
        levels.Level7(),
        levels.Level6(),
        levels.Level5(),
        levels.Level1(),
        levels.Level3(),
        levels.Level8(),
        levels.Level4(),
        levels.Level9(),
        levels.Level2()
    ]

    MENU_WIDTH = 200

    def __init__(self, width, height, fpsLock):
        self.width = width
        self.height = height
        self.fpsLock = fpsLock

        self.level = 0
        self.life = 3
        self.fps = 0
        self.timeTot = 0
        self.time = 0
        self.state = STATE.INITIAL

        self.gamefield = pygame.Surface((width - self.MENU_WIDTH, height))
        self.gamefield = self.gamefield.convert()

        self.menufield = pygame.Surface((self.MENU_WIDTH, height))
        self.menufield = self.menufield.convert()

        self.addButtons()
        
    def addButtons(self):
        self.fpsMessage  = Message((self.MENU_WIDTH-25, 15), str(self.fps))
        self.lifeMessage = Message((self.MENU_WIDTH/2, 60),
                                   "life: {}".format(self.life))
        self.levlMessage = Message((self.MENU_WIDTH/2, 90),
                                   "level: {}".format(self.level))
        self.timeMessage = Message((self.MENU_WIDTH/2, 120),
                                   "time: {0:.2f}/{1}".format(
                                       self.time / self.fpsLock, self.timeTot / self.fpsLock))
        self.endMessage = Message(((self.width - self.MENU_WIDTH)/2, self.height/2),
                                  "GAME OVER", size=60, color=(250,0,0))
        self.winMessage = Message(((self.width - self.MENU_WIDTH)/2, self.height/2),
                                  "WIN!",
                                  size=60, color=(247, 167, 111))
        
        pos, w, h = (self.MENU_WIDTH/2, 350), self.MENU_WIDTH*0.75, 40
        self.restartButton = Button(pos, w, h, "restart")
        
        pos, w, h = (self.MENU_WIDTH/2, 400), self.MENU_WIDTH*0.75, 40
        self.addNewMButton = Button(pos, w, h, "new missile")
        
        pos, w, h = (self.MENU_WIDTH/2, 200), self.MENU_WIDTH*0.75, 40
        self.nextLvlButton = Button(pos, w, h, "next level")
        
        pos, w, h = (self.MENU_WIDTH/2, 250), self.MENU_WIDTH*0.75, 40
        self.prevLvlButton = Button(pos, w, h, "prev. level")
        
        pos, w, h = (self.MENU_WIDTH/2, 300), self.MENU_WIDTH*0.75, 40
        self.pauseButton = Button(pos, w, h, "pause")
        
    def pause(self):
        if self.state == STATE.WAIT_UNTILL_STOP:
            self.state = STATE.PAUSE
            self.pauseButton.message.update("continue")
        elif self.state == STATE.PAUSE:
            self.state = STATE.WAIT_UNTILL_STOP
            self.pauseButton.message.update("pause")

    def lose(self):
        self.initLevel()
        self.life -= 1
        self.time = 0
        if self.life == 0:
            self.state = STATE.LOSS
        else:
            self.state = STATE.INITIAL

    def win(self):
        self.state = STATE.WIN
            
    def restart(self):
        self.initLevel()
        self.time = 0
        self.life = 3
        self.state = STATE.INITIAL

    def goToNextLevel(self):
        self.level = min(len(self.LEVELS) - 1, self.level + 1)
        self.restart()

    def goToPreviousLevel(self):
        self.level = max(0, self.level - 1)
        self.restart()
        
    def checkMenuSelection(self, pos):
        return pos[0] > self.width-self.MENU_WIDTH

    def checkButtonsSelection(self, pos):
        x, y = pos[0] - self.width + self.MENU_WIDTH, pos[1]
        self.restartButton.checkSelected((x,y))
        self.addNewMButton.checkSelected((x,y))
        self.nextLvlButton.checkSelected((x,y))
        self.prevLvlButton.checkSelected((x,y))
        self.pauseButton.checkSelected((x,y))
        
    def checkButtonsActivation(self, pos):
        x, y = pos[0] - self.width + self.MENU_WIDTH, pos[1]
        if self.restartButton.checkActivated((x,y)):
            self.restart()
        if self.addNewMButton.checkActivated((x,y)) and self.state not in (STATE.LOSS, STATE.WIN):
            self.state = STATE.INITIAL
        if self.nextLvlButton.checkActivated((x,y)):
            self.goToNextLevel()
        if self.prevLvlButton.checkActivated((x,y)):
            self.goToPreviousLevel()
        if self.pauseButton.checkActivated((x,y)):
            self.pause()
        
    def display(self, screen):
        self.gamefield.fill((116, 208, 242))
        self.menufield.fill((0, 109, 193))
        
        self.fpsMessage.update(str(self.fps))
        self.fpsMessage.display(self.menufield)
        self.lifeMessage.update("life: {}".format(self.life))
        self.lifeMessage.display(self.menufield)
        self.timeMessage.update("time: {0:.1f}/{1}".format(
            self.time / float(self.fpsLock), self.timeTot / self.fpsLock))
        self.timeMessage.display(self.menufield)
        self.levlMessage.update("level: {}".format(self.level + 1))
        self.levlMessage.display(self.menufield)
        
        self.restartButton.display(self.menufield)
        self.addNewMButton.display(self.menufield)
        self.nextLvlButton.display(self.menufield)
        self.prevLvlButton.display(self.menufield)
        self.pauseButton.display(self.menufield)
        
        self.world.display(self.gamefield)
        if self.state == STATE.LOSS:
            self.endMessage.display(self.gamefield)        
        if self.state == STATE.WIN:
            self.winMessage.display(self.gamefield)
            
        screen.blit(self.menufield, (self.width-self.MENU_WIDTH, 0))
        screen.blit(self.gamefield, (0, 0))
        
    def initLevel(self):
        width, height = self.width - self.MENU_WIDTH, self.height
        world = World(width, height)
        level = self.LEVELS[self.level]
        level.initialize(world)
        self.timeTot = level.MAX_TIME
        self.world = world
    
    def run(self, screen, fpsClock):
        self.initLevel()

        while True:
            if self.time == self.timeTot:
                self.lose()

            pos = pygame.mouse.get_pos()
            self.checkButtonsSelection(pos)

            if self.state == STATE.INITIAL:
                self.world.canon.setDirection(pos)
            elif self.state == STATE.CHOOSE_POWER:
                self.world.canon.setSpeed(pos)
            elif self.state == STATE.WAIT_UNTILL_STOP:
                self.world.canon.setDirection(pos)
                self.world.move(self.win, self.lose)
                self.time += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.checkMenuSelection(pos):
                        self.checkButtonsActivation(pos)
                    else:
                        if self.state == STATE.INITIAL:
                            self.state = STATE.CHOOSE_POWER
                            self.world.canon.state = 1
                        elif self.state == STATE.CHOOSE_POWER:
                            self.state = STATE.WAIT_UNTILL_STOP
                            self.world.canon.state = 2
                            self.world.addMissile()
                        elif self.state == STATE.LOSS:
                            self.restart()
                            continue
                        elif self.state == STATE.WIN:
                            self.goToNextLevel()
                            continue

            self.display(screen)
            pygame.display.update()
            self.fps = fpsClock.tick(self.fpsLock)
        