from pygame import Color,  Surface, sprite, image
from Object import Object
from math import sqrt
from random import randint

class Entity(Object):
    '''
    Entity class.

    On this turn we do a control for
    bots and players.
'''
    textures = ("textures/entities/EntityLeftRight.png",
                "textures/entities/EntityUpDown.png")
    w = 40
    h = 40
    
    def __init__(self, x = 0, y = 0,
                 hp = 100,
                 textures = textures,
                 w = w,
                 h = h):
        Object.__init__(self, x, y, textures[0], w, h)
        self.texLeftRight = image.load(textures[0]).convert()
        self.texUpDown = image.load(textures[1]).convert()
        self.hp = hp
        self.speed = 2
        self.mSpeed = 10

    def update(self,
               cam,
               platforms,
               left=False,
               right=False,
               up=False,
               down=False):
        """
        Called every tick. Change image position with
        camera's position and real position without
        camera.
"""
        if up:
            self.yVel -= self.speed
        elif down:
            self.yVel += self.speed
        else:
            self.yVel *= 0.7

        if up or down:
            self.image = self.texUpDown
        if left or right:
            self.image = self.texLeftRight

        if left:
            self.xVel -= self.speed
        elif right:
            self.xVel += self.speed
        else:
            self.xVel *= 0.7

        if self.xVel > self.mSpeed:
            self.xVel = self.mSpeed
        elif self.xVel < -self.mSpeed:
            self.xVel = -self.mSpeed

        if self.yVel > self.mSpeed:
            self.yVel = self.mSpeed
        elif self.yVel < -self.mSpeed:
            self.yVel = -self.mSpeed

        self.collide(self.xVel, self.yVel, platforms)
        self.realY += self.yVel
        self.realX += self.xVel

        self.rect.x = self.realX - cam.x
        self.rect.y = self.realY - cam.y

    def collide(self, xVel, yVel, platforms):
        """
        Check, is object colliding with something.
"""
        for p in platforms:
            if sprite.collide_rect(self, p):
                if xVel > 0:
                    self.rect.left = self.rect.right
                    self.xVel = 0
                    self.realX += -1.5 if p.realX > self.realX \
                                  else 1.5

                if xVel < 0:
                    self.rect.right = self.rect.left
                    self.xVel = 0
                    self.realX += -1.5 if p.realX > self.realX \
                                  else 1.5

                if yVel < 0:
                    self.rect.top = p.rect.bottom
                    self.yVel = 0
                    self.realY += -1.5 if p.realY > self.realY \
                                  else 1.5
                    
                if yVel > 0:
                    self.rect.bottom = p.rect.top
                    self.yVel = 0
                    self.realY += -1.5 if p.realY > self.realY \
                                  else 1.5

class Bot(Entity):
    '''
    Bot class.

    On this turn we do self-controlled entity.
'''
    agressive = True
    
    def __init__(self, x = 0, y = 0,
                 hp = 100, agr = agressive):
        Entity.__init__(self, x = 0, y = 0,
                        hp = 100)
        # Is a bot will be follow player?
        self.agr = agr
        self.speed = 0.3
        self.mSpeed = 6
    
    def updateAI(self, players, walls, cam):
        '''
        Found nearest player and go to them.
'''
        # if we are friendly bot,
        # update ai with another way.
        if not self.agr:
            self.updateAIFriendly(cam, platforms)
            return

        nearestPlayer = None
        nearestDist = None
        for player in players:
            currentDist = sqrt(player.realX*player.realX+player.realY*player.realY)
            if nearestDist is None:
                nearestDist = currentDist
                nearestPlayer = player
                continue
            if currentDist < nearestDist:
                nearestDist = currentDist
                nearestPlayer = player
        
        left = right = up = down = False

        if nearestPlayer.realX < self.realX \
           and abs(nearestPlayer.realX - self.realX) > 50:
            left = True
        if nearestPlayer.realX > self.realX \
           and abs(nearestPlayer.realX - self.realX) > 50:
            right = True
        if nearestPlayer.realY < self.realY \
           and abs(nearestPlayer.realY - self.realY) > 50:
            up = True
        if nearestPlayer.realY > self.realY \
           and abs(nearestPlayer.realY - self.realY) > 50:
            down = True

        self.update(cam,
                    walls,
                    left, right, up, down)
        if nearestDist < 10:
            self.attack()

    def updateAIFriendly(self, cam):
        # We do it in next generation
        self.update(cam)

    def attack(self):
        pass # TODO - create attack for bot

class NPS(Bot):
    """
    Bot class.

    It's friendly bot who doesn't
    hit players.
"""

    agressive = False

    def __init__(self, x = 0, y = 0,
                 hp = 100, agr = agressive):
        Bot.__init__(self, x = 0, y = 0,
                        hp = 100, agr = agr)
        # Is a bot will be follow player?
        self.agr = agr

    def updateAIFriendly(self, cam, platforms):
        '''
        Just move in random direction.
'''
        act = self.getRandomAction()
        self.update(cam,
                    platforms,
                    act[0],act[1],act[2],act[3])

    def getRandomAction(self):
        '''
        Model of moving is:

        1 2 3
        4 5 6
        7 8 9

        And now look on it like a joystick...
'''
        r = randint(1,8)
        left = True if r in (1, 4, 7) else False
        right = True if r in (3, 6, 9) else False
        up = True if r in (7, 8, 9) else False
        down = True if r in (1, 2, 3) else False
        return (left, right, up, down)

if __name__ == '__main__':
    while True:
        print("1 - Entity. \n2 - Bot. \n3 - NPS.")
        _in = input()
        if _in == '1':
            help(Entity)
        elif _in == '2':
            help(Bot)
        elif _in == '3':
            help(NPS)
        else:
            print('Unknown command.')

