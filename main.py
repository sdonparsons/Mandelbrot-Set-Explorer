#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Mandelbrot Set Viewer with zoom and explore functionality, by Sam D Parsons.

This is an application that computes the Mandelbrot set and then employs
pygame functionality to display the results to the user. This current
version supports click and zoom. Clicking on a location on the screen will
simultaneously center that location in the screen, and double the current
level of zoom (i.e. shrink the axes by a relative factor of two).

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Sam D Parsons"
__contact__ = "s-----@gmail.com"
__copyright__ = "Copyright $2023, $Sam D Parsons"
__credits__ = ["Sam D Parsons"]
__date__ = "2023/05/22"
__deprecated__ = False
__email__ = "s------@gmail.com"
__license__ = "GPLv3"
__maintainer__ = "Sam D Parsons"
__status__ = "Prototype"
__version__ = "0.0.3"

# Other libraries
import pygame

pygame.init()

MAX_COLOUR = 255

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


full_screen = False
if full_screen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    SCREEN_W = screen.get_rect().width
    SCREEN_H = screen.get_rect().height
    RESOLUTION = (SCREEN_W, SCREEN_H)
else:
    SCREEN_W = 800  # Screen width
    SCREEN_H = 500  # Screen height
    RESOLUTION = (SCREEN_W, SCREEN_H)
    screen = pygame.display.set_mode(RESOLUTION)

pygame.display.set_caption("Mandelbrot Set Viewer")
window_icon = pygame.image.load('icon.png')
pygame.display.set_icon(window_icon)

COLOUR_SCALE_X = MAX_COLOUR / SCREEN_W
COLOUR_SCALE_Y = MAX_COLOUR / SCREEN_H

r = 255
g = 255
b = 255

# Initial Mandelbrot display axes.
RE_START = -2
RE_END = 1

IM_START = -1.5
IM_END = 0.5


def truncate(n):
    return int(n * 1000) / 1000


def increase_colour(present_colour, increment):
    new_colour = present_colour
    if (present_colour + increment) <= 255:
        new_colour += increment
    else:
        new_colour = (present_colour + increment) % (255 + 1)
    return new_colour


class Mandelbrot():
    """A class to handle the definition of the Mandelbrot set."""
    def __init__(self):
        self.max_iter = 30

    # Return the number of iterations where number escapes.
    def iterations(self, c):
        z = 0
        n = 0
        while abs(z) <= 2 and n < self.max_iter:
            z = z*z + c
            n += 1
        return n

    # Increase the number of iterations computed.
    def increase_iter(self, increase):
        self.max_iter += increase


class Axes:
    """Class to represent the Re and Im axes for the Mandelbrot set."""
    def __init__(self):
        # Real axes start and end values.
        self.re_s = RE_START
        self.re_e = RE_END
        # Imaginary axes start and end values.
        self.im_s = IM_START
        self.im_e = IM_END

        self.width = 3
        self.height = 2

    def return_width(self):
        the_axes_width = self.re_e - self.re_s
        return the_axes_width

    def return_height(self):
        print("_________________________________________________")
        print(f"im_s: {self.im_e}_________________________________________________")
        print(f"im_e: {self.im_s}_________________________________________________")
        print("_________________________________________________")
        the_axes_height = self.im_e - self.im_s
        print(f"im_e - im_s = {the_axes_height}_________________________________________________")
        return the_axes_height


def zoom(axes_obj, mandel_obj):
    axes_obj.re_s = axes_obj.re_s / 2
    axes_obj.re_e = axes_obj.re_e / 2

    axes_obj.im_s = axes_obj.im_s / 2
    axes_obj.im_e = axes_obj.im_e / 2


def move_zoom(axes, mandelbrot_obj, x_click, y_click):
    axes_width = axes.return_width()
    axes_height = axes.return_height()

    # Convert pixel co-ordinates into axis values.
    mandelbrot_x_axis = axes.re_s + ((axes_width / SCREEN_W) * x_click)
    mandelbrot_y_axis = axes.im_s + ((axes_height / SCREEN_H) * (SCREEN_H - (y_click + 1)))

    axes.re_s = mandelbrot_x_axis - (axes_width / 4)
    axes.re_e = mandelbrot_x_axis + (axes_width / 4)

    axes.im_e = mandelbrot_y_axis + (axes_height / 4)
    axes.im_s = mandelbrot_y_axis - (axes_height / 4)

    mandelbrot_obj.increase_iter(10)


# Create the axes for the Mandelbrot set.
axes = Axes()
# Create a class to handle the set functions.
mand = Mandelbrot()

# Create a blank 3D array to represent the screen as x, y coordinates, with assigned RGB values.
y = []
for y_pos in range(SCREEN_H):
    x = []
    for x_pos in range(SCREEN_W):
        colour = [0, 0, 0]
        x.append(colour)
    y.append(x)


# Method to draw the mandelbrot to the pygame.screen object.
def draw_mandelbrot():
    pixel_colour = [0, 0, 0]
    colour_grad_y = 0
    for y_coordinate, x_coordinates in enumerate(y):
        y_inverted_axis = SCREEN_H - (y_coordinate + 1)  # To draw from negative imaginary to positive
        colour_grad_y = increase_colour(colour_grad_y, COLOUR_SCALE_Y)
        for x_coordinate, colour in enumerate(x_coordinates):
            c = complex(axes.re_s + (x_coordinate / SCREEN_W) * (axes.re_e - axes.re_s),
                        axes.im_s + (y_inverted_axis / SCREEN_H) * (axes.im_e - axes.im_s))
            # Calculating number of iterations.
            m = mand.iterations(c)
            # Colouring dependent on iterations.
            hue = ((m / mand.max_iter) * 180) + 75
            value = hue if m < mand.max_iter else 0
            colour_grad = value * 0.4
            colour_grad2 = value * 0.4
            colour_grad3 = value * 0.9

            # Turn y_grad black if in set.
            y_grad = colour_grad_y if m < mand.max_iter else 0

            pixel_colour = [y_grad, colour_grad3, colour_grad2]
            # Set the pygame (x, y) pixel colour.
            screen.set_at((x_coordinate, y_coordinate), pixel_colour)


# Draw the initial mandelbrot
draw_mandelbrot()

done = False
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()

            def mouse_debugging():
                width = axes.width
                height = axes.height
                print(f"Axes w/h: ({width}, {height})")
                print(f"Re start end: ({axes.re_s}, {axes.re_e})")
                mandelbrot_x_axis = truncate(axes.re_s + ((width / SCREEN_W) * pos[0]))
                mandelbrot_y_axis = truncate(axes.im_s + ((height / SCREEN_H) * (SCREEN_H - (pos[1] + 1))))
                print(f"({pos[0]},{pos[1]}), Re({mandelbrot_x_axis}), Im({mandelbrot_y_axis})")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                zoom(axes, mand)
                draw_mandelbrot()
            if event.key == pygame.K_q:
                done = True
            if event.key == pygame.K_r:
                axes.__init__()
                mand.__init__()
                draw_mandelbrot()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            x_click = mouse_pos[0]
            y_click = mouse_pos[1]
            move_zoom(axes, mand, x_click, y_click)
            draw_mandelbrot()
    pygame.display.flip()
pygame.quit()
