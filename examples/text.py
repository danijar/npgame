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


colors = Fading((9, 4), 0.5)
timer = 0

game = npgame.Game(grid=(11, 11), scale=40)
game.title('Text')
while game.running:
  game.update()

  if game.pressed('escape'):
    game.close()

  game.draw(0, 0, 40, 30, (0.5, 0.5, 0.5))  # Gray background

  # Fading text of random colors
  c = colors(game.delta)
  font = pathlib.Path(__file__).parent / 'font.ttf'
  for i, pos in enumerate(range(1, 10)):
    game.text(1, pos, 'Hello World!', font, c[i], pos / 7)
