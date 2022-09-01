import pathlib

import npgame
import numpy as np


class Fading:

  def __init__(self, shape, speed):
    self.speed = speed
    self.start = np.random.uniform(0, 1, shape)
    self.target = np.random.uniform(0, 1, shape)
    self.timer = 0

  def __call__(self, delta):
    self.timer += delta * self.speed
    if self.timer > 1:
      self.start = self.target
      self.target = np.random.uniform(0, 1, self.target.shape)
      self.timer = 0
    return (1 - self.timer) * self.start + self.timer * self.target


colors = Fading((9, 3), 0.5)
noise = Fading((9, 32, 32, 3), 2.0)
timer = 0

game = npgame.Game(grid=(11, 11), scale=40)
game.title('Graphics')
while game.running:
  game.update()

  if game.pressed('escape'):
    game.close()

  game.draw(0, 0, 40, 30, (0.5, 0.5, 0.5))  # Gray background

  # Fading boxes of random colors
  c = colors(game.delta)
  for i, pos in enumerate(range(1, 10)):
    game.draw(pos, 9, 0.8, 0.8, c[i])

  # Yellow boxes of increasing distance
  for pos in np.linspace(1, np.sqrt(9), 9):
    game.draw(pos ** 2, 8, 0.5, 0.5, (1, 0.7, 0))

  # Green boxes of increasing size
  for pos in range(1, 10):
    game.draw(pos, 7, pos / 10, pos / 10, (0, 0.7, 0))

  # Random arrays of increasing size
  n = noise(game.delta)
  for i, pos in enumerate(range(1, 10)):
    game.draw(pos, 6, pos / 10, pos / 10, array=n[i])

  # Images of increasing size
  n = noise(game.delta)
  image = pathlib.Path(__file__).parent / 'joystick_gray.jpg'
  for i, pos in enumerate(range(1, 10)):
    game.draw(pos, 5, pos / 10, pos / 10, image=image)

  # Images of increasing size
  n = noise(game.delta)
  image = pathlib.Path(__file__).parent / 'joystick_rgb.gif'
  for i, pos in enumerate(range(1, 10)):
    game.draw(pos, 4, pos / 10, pos / 10, image=image)

  # Images of increasing size
  n = noise(game.delta)
  image = pathlib.Path(__file__).parent / 'joystick_rgba.png'
  for i, pos in enumerate(range(1, 10)):
    game.draw(pos, 3, pos / 10, pos / 10, image=image)

  # Alpha blending and moving
  timer += game.delta
  image = pathlib.Path(__file__).parent / 'joystick_rgba.png'
  color = tuple(c[0]) + (0.6,)
  game.draw(0.8, 0.8, 1.3, 1.3, array=n[0])
  game.draw(1 + 0.2 * np.sin(5 * timer), 1, 1.5, 1.5, image=image)
  game.draw(1.3, .7 + 0.1 * np.sin(3 * timer), 1, 1, color=color)
  game.draw(1.5, .5, 1, 1, image=image)
