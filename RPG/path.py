from collections import namedtuple

Point = namedtuple("Point","x,y")

class ScreenPoint(list):
    def __init__(self, point, screen_width, screen_height):
        x, y = point
        list.__init__(self, [int(x*screen_width), int((1-y)*screen_height)])

class RoomPath:
    def __init__(self, path_function, 
        screen_width = 1024, screen_height = 768):
        self.path_function = path_function 
        self.screen_width, self.screen_height = screen_width, screen_height

    def get_position(self, x, y):
        relative_point = self.path_function(x = x , y = y, 
            width = self.screen_width, height = self.screen_height)
        return ScreenPoint(relative_point, screen_width = self.screen_width,
                            screen_height  = self.screen_height)



def depth_path(x, y, width, height):
    x, y = x/width , y/height
    if 0<=x<0.3:
        return Point(x = x, y = (x*.1 + y))
    if 0.3<=x<=0.7:
        return Point(x = x, y = (0.03 + y))
    if 0.7<x<=0 :
        return Point(x = x, y = (0.03 - (x-.7)*.1 + y))

    raise Exception("Invalid Location : ({},{})", x, y)

street = RoomPath(depth_path)