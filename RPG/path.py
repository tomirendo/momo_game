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
    bound = 0.05
    steep = 0.23
    min_area = 0.3
    max_area = 0.7
    if x<min_area:
        return Point(x = x*.8+bound, y = x*steep + bound)
    if min_area<=x<=max_area:
        return Point(x = x*.8 +bound, y = min_area*steep +bound)
    if max_area<x :
        return Point(x = x*.8+bound, y = (min_area - (x-max_area))*steep+bound)

    raise Exception("Invalid Location : ({},{})", x)

def stationary_path(fixed_position):
    def path(location):
        return fixed_position
    return path

def street(screen_width, screen_height):
    return RoomPath(depth_path, screen_width, screen_height)

def theater(screen_width, screen_height):
    return RoomPath(stationary_path([0.8,0.25]), screen_width, screen_height)