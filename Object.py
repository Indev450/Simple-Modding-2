from pygame import sprite, Surface, Rect, Color, image

class Object(sprite.Sprite):
    '''
    Top level class.

    Any object who can move on screen
    with camera.
'''
    
    texture = "textures/level/Block.png"
    w = 60
    h = 60

    def __init__(self,
                 x = 0,
                 y = 0,
                 texture = texture,
                 w = w, h = h):
        self.speed = 10
        self.xVel = 0
        self.yVel = 0
        self.speedDown = 0.5

        self.image = image.load(texture).convert()

        self.rect = Rect(x,
                         y,
                         w,
                         h)

        # To send for client
        self.realX = x
        self.realY = y

    def onDownPressed(self):
        """
        Called if 'down' in update.
"""
        return 10

    def onUpPressed(self):
        """
        Called if 'up' in update.
"""
        return -10

    def update(self,
               cam,
               left=False,
               right=False,
               up=False,
               down=False):
        """
        Called every tick. Change image position with
        camera's position and real position without
        camera.
"""
        
        if left:
            self.xVel = -self.speed
        if right:
            self.xVel = self.speed

        # If we don't press -> or <-,
        # decrement speed.
        if not(left or right):
            self.xVel *= self.speedDown
            if self.xVel < 0.1 and self.xVel > -0.1:
                self.xVel = 0

        self.yVel += self.onDownPressed() if down \
                     else self.onUpPressed if up \
                     else 0

        # Change our real coordinates
        # and then change coordinates
        # on screen.
        self.realX += self.xVel
        self.realY += self.yVel
        self.rect.x = self.realX - cam.x
        self.rect.y = self.realY - cam.y
        
        self.yVel *= self.speedDown

    def draw(self, screen):
        """
        Draw self on screen if we don't out of
        it.
"""
        if self.rect.x < -60 or \
           self.rect.x > 1084 or \
           self.rect.y < -60 or \
           self.rect.y > 900:
            return
        screen.blit(self.image, (self.rect.x,self.rect.y))

    def getInfo(self):
        '''
        Send our data for connected players.
'''
        return {'position':(self.realX, self.realY),
                'color':self.color}

if __name__ == '__main__':
    help(Object) # Show info if script started separately.
    _ready = None
    _ready = input()
