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

    def get_position(self, location):
        return ScreenPoint(self.path_function(location =  location),   
                            screen_width = self.screen_width,
                            screen_height  = self.screen_height)



def depth_path(location):
    x  = location
    bound = 0.1
    if x<0.3:
        return Point(x = x*.8+bound, y = x + bound)
    if 0.3<=x<=0.7:
        return Point(x = x*.8+bound, y = 0.3 +bound)
    if 0.7<x :
        return Point(x = x*.8+bound, y = (0.3 - (x-.7))+bound)
    return Point(0.7+bound, y = bound)

    raise Exception("Invalid Location : ({},{})", x)

street = RoomPath(depth_path)