

'''
a simple snake game based on termbox
'''
import termbox
from collections import deque
from random import randint, choice
import time


def print_line(screen, msg):
    '''print a msg at the top of the screen for debugging'''
    for i in range(len(msg)):
        screen.change_cell(i, 0, ord(msg[i]), termbox.WHITE, termbox.BLACK)


class snake(object):

    def __init__(self):
        self.body = deque()
        self.body_set = set(self.body)
        self.length = 0
        self.screen = None
        self.char = ord('#')

    def generate_random_body(self, length):
        screen = self.screen
        w = screen.width()
        h = screen.height()

        body = deque()

        body_segment = (randint(0, w-1), randint(0, h-1))
        body.append(body_segment)
        for i in range(1, length):
            if body[-1][0] + 1 < w:
                body_segment = (body[-1][0] + 1, body[-1][1])
                body.append(body_segment)

        self.set_body(body)

    def set_body(self, body):
        self.body = body
        self.length = len(body)
        self.body_set = set(body)

    def draw(self):
        screen = self.screen
        if self.length == 0:
            return

        # draw first as red
        screen.change_cell(self.body[0][0], self.body[0][1],
                           self.char, termbox.RED, termbox.BLACK)

        for i in range(1, len(self.body)):
            s = self.body[i]
            # s[0] - x coord; s[1] - y coord
            screen.change_cell(s[0], s[1], self.char, termbox.WHITE, termbox.BLACK)

    def move_body(self, body_segment):

        self.body.appendleft(body_segment)
        self.body_set.add(body_segment)
        self.body_set.remove(self.body.pop())

    def set_screen(self, screen):
        self.screen = screen

    def reset(self):

        self.generate_random_body(30)

    def move(self, direction, dry=False):
        screen = self.screen
        body = self.body

        if direction == 'up':
            new_bs = (body[0][0], body[0][1] - 1)
        elif direction == 'down':
            new_bs = (body[0][0], body[0][1] + 1)
        elif direction == 'left':
            new_bs = (body[0][0] - 1, body[0][1])
        elif direction == 'right':
            new_bs = (body[0][0] + 1, body[0][1])
        else:
            new_bs = None

        print_line(screen, 'newbs: %d %d, w:%d, h:%d' %
                   (new_bs[0], new_bs[1], screen.width(), screen.height()))

        if self.length > 1 and new_bs == body[1]:
            # do nothing
            if dry:
                return True
        elif new_bs[0] < 0 or new_bs[0] >= screen.width():
            if dry:
                return False
            else:
                self.reset()
        elif new_bs[1] < 0 or new_bs[1] >= screen.height():
            if dry:
                return False
            else:
                self.reset()
        elif new_bs in self.body_set:
            if dry:
                return False
            else:
                self.reset()
        else:
            if dry:
                return True
            else:
                self.move_body(new_bs)

    def dance(self):
        '''generate a direction that I can move to'''
        possible_directions = ['up', 'down', 'left', 'right']

        for direction in possible_directions:
            if not self.move(direction, dry=True):
                possible_directions.remove(direction)

        if len(possible_directions) == 0:
            self.reset()
        else:
            direction = choice(possible_directions)
            self.move(direction)


if __name__ == '__main__':
    s = snake()
    screen = termbox.Termbox()
    s.set_screen(screen)
    s.generate_random_body(10)
    run = True

    while run:
        event = screen.peek_event()
        if event:
            tp, ch, key, mod, w, h, x, y = event
            if tp == termbox.EVENT_KEY and key == termbox.KEY_ESC:
                run = False

        screen.clear()
        s.dance()
        s.draw()
        screen.present()
        time.sleep(0.1)
