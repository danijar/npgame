[![PyPI](https://img.shields.io/pypi/v/npgame.svg)](https://pypi.python.org/pypi/npgame/#history)

🕹️ npgame
=========

`npgame` makes it easy and fast to write simple games, powered by Numpy and
PyGame. It's a lightweight API to quickly get something done and for learning
rather than a solution full-blown feature-rich games.

Features include opening a window, showing graphics like colored rectangles and
images, and detecting keyboard input. For additional features like mouse input
and audio, check out PyGame, which can be combined freely.

Installation
------------

```sh
pip install npgame
```

Quickstart
----------

```python
import npgame

# Initialize state
pos = 5.5

game = npgame.Game(grid=(20, 15), scale=40)
game.title('Quickstart')
while game.running:
  game.update()

  # Update state
  if game.pressed('escape'):
    game.close()
  if game.pressed('a'):
    pos -= game.delta * 2.0
  if game.pressed('d'):
    pos += game.delta * 2.0

  # Display
  game.draw(0, 0, 40, 30, (1, 1, 1))  # White background
  game.draw(pos, 3.4, 1.5, 1.5, (1, 0.7, 0))  # Yellow box
```

Conventions
-----------

Coordinates mimic the convention for numeric charts. In other words, X is the
horizontal axis and Y is the vertical axis and zero is in the lower left corner
of the window. The size of the coordinate system is specified with
`Game(grid=(40, 30))`.

Documentation
-------------

### `npgame.Game(grid=(40, 30), scale=20, fps=60)`

Create a Game object that processes keyboard events and graphics for us. The
`grid` determines the size of coordinate system for drawing. The `scale` sets
the size of each grid tile in pixels. It also determines the window size. The
`fps` set the maximum number of frames per second, beyond which `update()` will
add a pause.

#### Attributes

- ### `running`

  Boolean attribute that signals whether the game is still running. This should
  be used as condition in the main loop. Closing the game window or calling
  `close()` switches the flag to `False`.

- ### `delta`

  Float attribute that contains the time that has passed between the last two
  `update()` calls. When moving objects, this value should be used to multiply
  the velocities to ensure that objects move at constant speed regardless of
  how fast the computer is. Multiplying velocities by `delta` effectively gives
  them the unit of grid tiles per second.

#### Methods

- ### `title(text)`

  Set the title of the window. This can be called either once in the beginning or
  repeatedly later on, for example to display status information to the user.

- ### `update()`

  This function should be called early inside the main loop. It displays the
  things that have been drawn and processes external events, such as key presses
  and checks whether the window has been closed.

- ### `pressed(key)`

  Returns a boolean indicating whether the given key is pressed. The requested
  key is passed in as a string, corresponding to the [pygame key name][keynames].
  The function detects both keys that are currently held down and keys that were
  briefly pressed between the last two `update()` calls.

- ### `draw(x, y, w, h, color=None, array=None, image=None)`

  Draws a rectangle of a color given as RGB tuple, an Numpy array, or an image
  given as string path. The position of the area is specified with `x` and `y`
  and its size with `w` and `h`. Images are resized as needed and cached for
  efficiency. For the area to appear, `update()` must be called inside the main
  loop.

- ### `close()`

  Shuts down pygame, which closes the window, and sets `running` to `False` so
  that the main loop ends.
