class SquareType(type):
    def __instancecheck__(self, instance):
        return instance[0] in range(8) and instance[1] in range(8)

class Square(metaclass=SquareType):
    pass

Move = tuple[Square, Square]

WHITE = 'white'
BLACK = 'black'

# Create a custom Color type
class ColorType(type):
    def __instancecheck__(self, instance):
        return instance in {WHITE, BLACK}

# Assign the Colour type
class Color(metaclass=ColorType):
    pass
