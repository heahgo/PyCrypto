class Point:

    def __init__(self, x, y):
        self.x, self.y = x, y  
        
    def infinity():
        return Point(None, None) # Point(None, None) : Point at infinity
    
    def equal(self, p):
        if self.x == p.x and self.y == p.y:
            return True
        else:
            return False
        
    def isInfinity(self):
        if self.equal(Point.infinity()):
            return True
        else:
            return False

    def show(self):
        if self.isInfinity():
            print('Point at infinity')
            return
        print(f'({self.x}, {self.y})')