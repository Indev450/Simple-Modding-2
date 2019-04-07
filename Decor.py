from Object import Object
from pygame import Surface, image
from random import randint

class Decor(Object):
    '''
    Decor class.

    Used for do levels more beutiful...
'''
    textures = ("textures/decor/flower.png",)
    w = 20
    h = 20

    def __init__(self, x = 0,
                 y = 0, textures = textures,
                 w = w, h = h):
        Object.__init__(self,x,y,textures[0],w,h)
