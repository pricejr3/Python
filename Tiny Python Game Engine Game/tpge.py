"""
Tiny Python Game Engine

This module provides a very simple Python game engine for writing elementary
turn based games with primitive 2D graphics in a 640x480 window.

LICENSE: This is open-source software released under the terms of the
BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause).

PLATFORMS: This module provides a wrapper around John Zelle's graphics
library (http://mcsp.wartburg.edu/zelle/python/graphics.py).

INSTALLATION: Put this file somewhere where Python can see it.

OVERVIEW: TPGE games function in a 640x480 window whose origin is in the
lower left corner, and make use of the following data model:
- A Point is a pair (X,Y) of integers where 0 <= X <= 640 and
  0 <= Y <= 480.
- A Color is one of the constants RED, BLUE, GREEN, BLACK, or YELLOW.
- A Line Segment is a 4-tuple (X1,Y1,X2,Y2) where (X1,Y1) and (X2,Y2) are
  points.
- A Circle is a triple (X,Y,R) of integers where (X,Y) describe a point
  and R defines the radius of the circle.
- A Rectangle is a 5-tuple (X1,Y1,X2,Y2,C) where (X1,Y1) and (X2,Y2) are
  points defining the opposite corners of a rectangle and C is a Color
  defining the Rectangle's fill color.
- A Text is a 4-tuple (S,X,Y,H) where S is a string, (X,Y) describe a point
  on which the text is centered, and H is an integer in the interval [5,37)
  defining the font size to be used in drawing the text.
- An Image is either a Line Segment, a Circle, Rectangle, or a Text.
- An Image List is a list of Images.
- A State is whatever kind of Python data structure the game developer
  chooses.

The engine assumes that the following functions will be defined by the
game developer:
- initial_state : State
  initial_state() returns the initial state of the game.
- successor_state : State x Point -> State
  successor_state(S,P) returns the successor state of the game resulting
  from clicking point P in state S.
- game_over : State -> Boolean
  game_over(S) is true if and only if the game is over in state S.
- images : State -> Image List
  images(S) is the list of Images that need to be drawn to the screen in
  order to present the state S to the user.
- game_title : String
  game_title() returns the name of the game which serves as the window
  title
"""

from graphics import *

WIDTH  = 640
HEIGHT = 480

CIRCLE = -1
LINE_SEGMENT = -2
TEXT = -3
RECTANGLE = -4

RED = "red"
BLUE = "blue"
GREEN = "green"
BLACK = "black"
YELLOW = "yellow"

def convert(I):
    """
    convert : Image -> Zelle Graphics Object
    If I is an Image, then convert(I) is the corresponding graphics
    object in the John Zelle Graphics Library.
    """
    if image_type(I) == CIRCLE:
        return convert_circle(I)
    elif image_type(I) == RECTANGLE:
        return convert_rectangle(I)
    elif image_type(I) == LINE_SEGMENT:
        return convert_line(I)
    elif image_type(I) == TEXT:
        return convert_text(I)

def image_type(I):
    """
    image_type : Image -> {CIRCLE, LINE_SEGMENT, TEXT}
    If I is a TPGE Image, then image_type(I) is an element of the set
    {CIRCLE, LINE_SEGMENT, TEXT}.
    """
    if len(I) == 3:
        return CIRCLE
    elif len(I) == 5:
        return RECTANGLE
    elif type(I[0]) == str:
        return TEXT
    elif type(I[0]) == int:
        return LINE_SEGMENT

def convert_circle(I):
    """
    convert_circle : Circle -> Zelle Graphics Object
    If I is a TPGE Circle then convert_circle(I) is the corresponding
    object in the John Zelle Graphics Library.
    """
    C = Point(I[0], HEIGHT - I[1])
    R = I[2]
    return Circle(C, R)

def convert_rectangle(I):
    """
    convert_rectangle : Rectangle -> Zelle Graphics Object
    If I is a TPGE Rectangle then convert_rectangle(I) is the corresponding
    object in the John Zelle Graphics Library.
    """
    P1 = Point(I[0], HEIGHT - I[1])
    P2 = Point(I[2], HEIGHT - I[3])
    C = I[4]
    R = Rectangle(P1, P2)
    R.setFill(C)
    return R

def convert_line(I):
    """
    convert_line : Line -> Zelle Graphics Object
    If I is a TPGE Line then convert_line(I) is the corresponding
    object in the John Zelle Graphics Library.
    """
    P1 = Point(I[0], HEIGHT - I[1])
    P2 = Point(I[2], HEIGHT - I[3])
    return Line(P1, P2)

def convert_text(I):
    """
    convert_text : Circle -> Zelle Graphics Object
    If I is a TPGE Text then convert_text(I) is the corresponding
    object in the John Zelle Graphics Library.
    """
    C = Point(I[1], HEIGHT - I[2])
    S = I[0]
    H = I[3]
    T = Text(C, S)
    T.setSize(H)
    return T

def game_canvas(Title):
    """
    game_canvas : (None -> String) -> Zelle Graphics Window
    If Title is a string denoting the name the of game, then
    game_canvas(Title) is the Zelle Graphics Window object in
    which the game is played.
    """
    return GraphWin(Title, WIDTH, HEIGHT)

def run_game(game_title, initial_state, successor_state, game_over, images):
    """
    Defines a procedure describing the main loop of a TPGE game. The
    procedure takes as its arguments the following functions:
    - game_title : String
    game_title() returns the name of the game which serves as the window
    title
    - initial_state : State
    initial_state() returns the initial state of the game.
    - successor_state : State x Point -> State
    successor_state(S,P) returns the successor state of the game resulting
    from clicking point P in state S.
    - game_over : State -> Boolean
    game_over(S) is true if and only if the game is over in state S.
    - images : State -> Image List
    images(S) is the list of Images that need to be drawn to the screen in
    order to present the state S to the user.
    """
    # create a window in which the game is played
    Canvas = game_canvas(game_title())

    # obtain the intial state and its corresponding graphics
    State = initial_state()
    Graphics = [convert(Image) for Image in images(State)]
    try:
        while not game_over(State):
            # draw every graphic for the current state to the game canvas
            for Graphic in Graphics:
                Graphic.draw(Canvas)

            # obtain the current mouse click as a Point object
            Click = Canvas.getMouse()
            Point = (Click.getX(), HEIGHT - Click.getY())

            # obtain the successor state
            State = successor_state(State, Point)

            # clear the canvas of all graphical objects
            for Graphic in Graphics:
                Graphic.undraw()

            # obtain the graphics for the current state
            Graphics = [convert(Image) for Image in images(State)]
        Canvas.close()
    except GraphicsError:
        Canvas.close()
