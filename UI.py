from pygame import sprite, Surface, Rect, Color, image


class Button(sprite.Sprite):
    '''
    UI class.

    Used for do some button with function.
'''
    
    def __init__(self, x, y,
                 w, h,
                 function,
                 texOnRelease,
                 texOnPress,
                 owner = None):
        
        self.owner = owner
        self.x = x
        self.y = y
        self.image = image.load(texOnRelease).convert()
        self.pressedImage = image.load(texOnPress).convert()

        self.rect = Rect(x, y, w, h)

        self.function = function
        self.currentImage = self.image

        self.visible = True
        
        if self.owner is not None:
            self.visible = self.owner.visible

    def update(self, click = None):
        if self.owner is not None:
            self.visible = self.owner.visible
            
        if not self.visible: return
        
        if click is not None:
            x, y = click.pos
            if self.rect.collidepoint(x, y):
                self.currentImage = self.pressedImage
                self.function()
        else:
            self.currentImage = self.image

    def draw(self, screen):
        if not self.visible: return
        
        screen.blit(self.currentImage, (self.rect.x, self.rect.y))

class Widget(sprite.Sprite):

    def __init__(self, x, y, w, h,
                 texture,
                 parent = None,
                 visible = False):
        self.rect = Rect(x, y, w, h)
        self.parent = parent
        self.visible = visible
        self.image = image.load(texture).convert()

    def update(self, screen):
        if self.visible:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.parent is None:
            return
        self.visible = self.parent.visible

class UI:
    '''
    UI class.

    Contains and controls buttons on screen.
'''

    def __init__(self):
        exitButton = Button(974, 10, 40, 40, quit,
                            texOnRelease = "textures/UI/exitButtonRelease.png",
                            texOnPress = "textures/UI/exitButtonPress.png")
        menu = Widget(360, 200, 100, 250, visible = False, texture = "textures/UI/menu.png")
        openMenuButton = Button(10, 10, 200, 160, self._setMenu,
                                texOnRelease = "textures/UI/ButtonMenuReleased.png",
                                texOnPress = "textures/UI/ButtonMenuPressed.png")
        
        self.hide = False
        self.buttons = [exitButton, openMenuButton]
        self.widgets = [menu]

    def _setMenu(self):
        self.widgets[0].visible = self.widgets[0].visible == False # Inverting

    def update(self, screen, click = None):
        if self.hide: return
        list(map(lambda x: x.update(click), self.buttons))
        list(map(lambda x: x.draw(screen), self.buttons))
        list(map(lambda x: x.update(screen), self.widgets))

    def setHide(self):
        self.hide = self.hide == False
