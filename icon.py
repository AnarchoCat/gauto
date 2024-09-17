import utils
class Icon:
    pool = {}

    @staticmethod
    def create(img):
        if img in Icon.pool:
            return Icon.pool[img]
        icon = Icon(img)
        Icon.pool[img] = icon
        return icon

    def __init__(self, img) -> None:
        self._img = img
        self._pos = None
    
    def locate(self):
        self._pos = utils.locate(self._img)
    
    def hover(self):
        if self._pos is None:
            self.locate()
        utils.moveTo(self._pos)
    
    def click(self):
        if self._pos is None:
            self.locate()
        utils.click(self._pos)
    
    def swipeLeft(self):
        self.hover()
        utils.swipeLeft()
    
    def swipeRight(self):
        self.hover()
        utils.swipeRight()