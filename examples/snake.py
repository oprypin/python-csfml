from __future__ import division

import random
import itertools
import collections

import pycsfml.all as sf


window = sf.RenderWindow(
    sf.VideoMode(800, 800, 32), "Snake", sf.Style.DEFAULT,
    sf.ContextSettings(depth=32, antialiasing=8), framerate_limit=10
)


class Direction:
    left = sf.Vector2(-1, 0)
    up = sf.Vector2(0, -1)
    right = sf.Vector2(1, 0)
    down = sf.Vector2(0, 1)
directions = [Direction.left, Direction.up, Direction.right, Direction.down]


def random_color():
    return sf.Color(*(random.randint(128, 255) for i in range(3)))


class Snake(collections.deque):
    def __init__(self, field, start=None, color=None):
        self.field = field

        if start is None:
            start = field.size//2

        for d in range(3):
            self.append(sf.Vector2(start.x, start.y+d))

        self.direction = Direction.up

        if color is None:
            color = random_color()
        self.color = color
    
    def turn(self, direction):
        if self[1]!=self[0]+direction:
            self.direction = direction
    
    def step(self):
        self.last = self.pop()
        self.appendleft(self[0]+self.direction)
        self[0].x %= field.size.x
        self[0].y %= field.size.y
    
    def grow(self, n=3):
        for i in range(n):
            self.append(self[-1])
    
    def draw(self, target, states):
        for i in range(len(self)):
            this = self[i]
            neighbors = []
            if i-1>=0:
                neighbors.append(self[i-1])
            if i+1<len(self):
                neighbors.append(self[i+1])
            
            circle = sf.CircleShape(0.9/2, fill_color=self.color)
            circle.position = this+(0.05, 0.05)
            target.draw(circle, states)
            
            # The following is eye candy and may be removed
            # but change the above to RectangleShape((0.9, 0.9), ...)

            # Look in 4 directions around this segment. If there is another one
            # neighboring it, draw a square between them
            for d in directions:
                td = this+d
                td = sf.Vector2(td.x%self.field.size.x, td.y%self.field.size.y)
                if td in neighbors:
                    rect = sf.RectangleShape((0.9, 0.9), fill_color=self.color)
                    rect.position = this+d/2+(0.05, 0.05)
                    target.draw(rect, states)
            
            # Draw eyes with a darkened color
            circle = sf.CircleShape(0.2/2)
            circle.fill_color = sf.Color(self.color.r//3, self.color.g//3, self.color.b//3)

            delta = (abs(self.direction.y)/4, abs(self.direction.x)/4)
            circle.position = self[0]+(0.4, 0.4)+delta
            target.draw(circle, states)

            circle.position = self[0]+(0.4, 0.4)-delta
            target.draw(circle, states)
            
    
    def collide_self(self):
        for part in self:
            if self[0]==part and part is not self[0]:
                return True
        return False
    
    def collide_snake(self, other):
        for part in other:
            if self[0]==part:
                return True
        return False
    
    def collide_food(self, food):
        return self[0]==food.position


class Food:
    def __init__(self, position, color=None):
        self.position = position

        if color is None:
            color = random_color()
        self.color = color
    
    def draw(self, target, states):
        circle = sf.CircleShape(0.9/2, fill_color=self.color)
        circle.position = self.position+(0.05, 0.05)
        target.draw(circle, states)



class Field:
    def __init__(self, size):
        self.size = sf.Vector2(*size)
        self.snakes = []
        self.foods = []
    
    def step(self):
        while len(self.foods)<len(self.snakes)+1:
            food = Food(sf.Vector2(random.randrange(self.size.x), random.randrange(self.size.y)))
            # Don't allow new food on top of a snake
            for snake in self.snakes:
                if snake.collide_food(food):
                    break
            else:
                self.foods.append(food)
        
        for snake in self.snakes:
            snake.step()
            if snake.collide_self():
                self.snakes.remove(snake)
            for food in self.foods:
                if snake.collide_food(food):
                    self.foods.remove(food)
                    snake.grow()
        for a, b in itertools.permutations(self.snakes, 2):
            if a.collide_snake(b):
                self.snakes.remove(a)

    def draw(self, target, states):
        for snake in self.snakes:
            snake.draw(target, states)
        for food in self.foods:
            food.draw(target, states)


field = Field((40, 40))

snake1 = Snake(field, field.size//2-(5, 0))
field.snakes.append(snake1)
snake2 = Snake(field, field.size//2+(5, 0))
field.snakes.append(snake2)

transform = sf.Transform().scale((20, 20))
states = sf.RenderStates(transform=transform)

player1_controls = [sf.Keyboard.A, sf.Keyboard.W, sf.Keyboard.D, sf.Keyboard.S]
player1_controls = dict(zip(player1_controls, directions))
player2_controls = [sf.Keyboard.LEFT, sf.Keyboard.UP, sf.Keyboard.RIGHT, sf.Keyboard.DOWN]
player2_controls = dict(zip(player2_controls, directions))

players = [(snake1, player1_controls), (snake2, player2_controls)]

while window.is_open:
    for event in window.events:
        if isinstance(event, sf.CloseEvent):
            window.close()
        
        if isinstance(event, sf.KeyEvent) and event.pressed:
            if event.code==sf.Keyboard.ESCAPE:
                window.close()
            
            for snake, controls in players:
                try:
                    snake.turn(controls[event.code])
                except KeyError:
                    pass
    
    field.step()
    window.clear(sf.Color.BLACK)
    window.draw(field, states)
    window.display()