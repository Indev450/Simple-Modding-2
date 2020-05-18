import socket as sk
import pickle as pkl
import json
import sys

try:
    import pygame as pg
except ImportError:
    print("Библиотека pygame не найдена, пробую установить...")
    try:
        import pip
        pip.main(["install", "pygame"])
    except ImportError:
        print("Не найден pip")
        raise SystemExit(-1)
    except Exception as e:
        print("Ошибка: %s" % str(e))
        raise SystemExit(-2)
    print("Pygame установлена, перезапустите игру")
    raise SystemExit(0)

from Bot import Bot, NPS, Entity
from Camera import Camera
from Object import Object
from Decor import Decor
from UI import UI


class Activity:
    '''
    Game class.

    In it we initialize pygame,
    level, entities, etc.
'''

    ui = None
    wW = 1024
    wH = 750
    wC = "#009900"
    wWH = (wW, wH)
    players = []
    NPS = []
    Bots = []
    walls = []
    bgDecor = []
    decor = []
    screen = None
    bg = None
    timer = None
    mPlayer = None
    camera = None

    @classmethod
    def preload(cls):
        print("Write file to load. If you wanna load\n"
              "default, just press enter.")
        try:
            filename = input('\nfile ->')
            file = open(filename)
        except FileNotFoundError:
            print('File \'' + filename + '\' is not found. Using default.')
            file = open('default.json')
        print('\nLoading file...')
        level = json.load(file)
        cls.spawn = level['spawn']
        x = y = 0
        file.close()
        print('\nSetting up pygame...')
        pg.init()
        cls.screen = pg.display.set_mode(Activity.wWH, pg.FULLSCREEN)
        pg.display.set_caption("Simple modding")
        cls.bg = pg.Surface(Activity.wWH)
        cls.bg.fill(pg.Color(cls.wC))
        cls.timer = pg.time.Clock()

        print('\nBuilding world...')
        for row in level['level']:
            for col in row:
                if col == "-":
                    cls.walls.append(Object(x, y))
                x += 60
            y += 60
            x = 0
        print("\nLoading finished.")

    @classmethod
    def spawnPlayer(cls, x, y, hp = 100):
        # If main player created.
        if cls.mPlayer is not None:
            cls.players.append(Entity(x, y, hp))
            print("Spawned player.")
            return
        # else.
        cls.mPlayer = Entity(120, 100, hp)
        print("Spawned main player.")

    @classmethod
    def spawnNPS(cls, x, y, hp = 100):
        cls.NPS.append(NPS(x, y, hp))
        print("Spawned NPS.")

    @classmethod
    def spawnBot(cls, x, y, hp = 100):
        cls.Bots.append(Bot(x, y, hp))
        print("Spawned bot.")

    @classmethod
    def setupCamera(cls):
        cls.camera = Camera(Activity.mPlayer)
        print("Camera setup: finished.")

    @classmethod
    def checkConnections(cls):
        pass

    @classmethod
    def addDecor(cls, decor, bg = False):
        if bg:
            cls.bgDecor.append(decor)
            return
        cls.decor.append(decor)

    @classmethod
    def activateUI(cls, ui):
        cls.ui = ui

    @classmethod
    def mainLoop(cls):
        left=right=up=down=False
        print("starting main loop.")
        while True:
            cls.timer.tick(80)
            click = None

            for e in pg.event.get():

                if e.type == pg.QUIT:
                    quit()

                if e.type == pg.MOUSEBUTTONDOWN:
                    click = e

                if e.type == pg.KEYDOWN and e.key == pg.K_z:
                    cls.ui.setHide()
            
                if e.type == pg.KEYDOWN and e.key == pg.K_LEFT:
                    left = True
                if e.type == pg.KEYUP and e.key == pg.K_LEFT:
                    left = False
                if e.type == pg.KEYDOWN and e.key == pg.K_RIGHT:
                    right = True
                if e.type == pg.KEYUP and e.key == pg.K_RIGHT:
                    right = False

                if e.type == pg.KEYDOWN and e.key == pg.K_UP:
                    up = True

                if e.type == pg.KEYUP and e.key == pg.K_UP:
                    up = False
                
                if e.type == pg.KEYDOWN and e.key == pg.K_DOWN:
                    down = True

                if e.type == pg.KEYUP and e.key == pg.K_DOWN:
                    down = False
                    
            cls.screen.blit(cls.bg, (0, 0))

            list(map(lambda x: x.update(cls.camera),cls.bgDecor))
            list(map(lambda x: x.draw(cls.screen),cls.bgDecor))

            list(map(lambda x: x.update(cls.camera),cls.walls))
            list(map(lambda x: x.draw(cls.screen),cls.walls))

            cls.mPlayer.update(cls.camera,
                               cls.walls,
                               left, right, up, down)
            cls.mPlayer.draw(cls.screen)
            cls.camera.updateWithObject()

            list(map(lambda x: x.updateAI(cls.players+[cls.mPlayer],
                                          cls.walls,
                                          cls.camera),cls.Bots))
            list(map(lambda x: x.draw(cls.screen),cls.Bots))

            list(map(lambda x: x.updateAIFriendly(cls.camera,
                                                  cls.walls),cls.NPS))
            list(map(lambda x: x.draw(cls.screen),cls.NPS))

            list(map(lambda x: x.update(cls.camera),cls.decor))
            list(map(lambda x: x.draw(cls.screen),cls.decor))

            cls.ui.update(cls.screen, click)
            
            pg.display.update()

Activity.preload()
Activity.activateUI(UI())
Activity.spawnPlayer(Activity.spawn[0], Activity.spawn[1], 100)
#Activity.spawnNPS(Activity.spawn[0], Activity.spawn[1], 100) # NPS is bad, i upgrade him... Once...
Activity.spawnBot(Activity.spawn[0], Activity.spawn[1], 100)
#Activity.addDecor(Decor(200, -40), bg = True)
Activity.setupCamera()
Activity.mainLoop()
