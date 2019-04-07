class Camera:
    '''
    Utility class.

    Can be pointed on object.
    Using for do levels a bigger.
'''

    def __init__(self, obj):
        self.x = obj.realX - 502
        self.y = obj.realY - 375
        self.obsObj = obj

    def updateWithObject(self):
        '''
        Update our coordinates with object-pointer.
'''
        self.x = self.obsObj.realX - 502
        self.y = self.obsObj.realY - 375

    def resetObject(self, obj):
        '''
        Set other object for observing.
'''
        self.obsObj = obj

if __name__ == '__main__':
    help(Camera) # Show info if script started separately.
    _ready = None
    _ready = input()
