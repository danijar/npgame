import time
import pathlib

import imageio
import numpy as np
import pygame
from PIL import Image


class Game:

  def __init__(self, grid=(40, 30), scale=20, fps=60):
    pygame.init()
    self.running = True
    self.delta = 0
    self._grid = grid
    self._scale = scale
    self._canvas = np.zeros((grid[0] * scale, grid[1] * scale, 3), np.float32)
    self._screen = pygame.display.set_mode(self._canvas.shape[:2])
    self._images = {}
    self._pressed = None
    self._keydowns = None
    self._fps = fps
    self._clock = pygame.time.Clock()
    self._time = time.time()

  def pressed(self, key):
    if not self._pressed:
      return False
    code = pygame.key.key_code(key)
    return self._pressed[code] or code in self._keydowns

  def draw(self, x, y, w, h, color_or_image):
    x, y = int(x * self._scale), int(y * self._scale)
    w, h = int(w * self._scale), int(h * self._scale)
    x1, x2, y1, y2 = x, x + w, y, y + h
    x1, x2 = max(0, x1), min(x2, self._canvas.shape[0])
    y1, y2 = max(0, y1), min(y2, self._canvas.shape[1])
    if x2 - x1 < 1 or y2 - y1 < 1:
      return
    if isinstance(color_or_image, str):
      image = self._image(color_or_image, (w, h))
      image = image[x1 - x: x2 - x, y1 - y: y2 - y]
      self._canvas[x1: x2, y1: y2] = image
    else:
      self._canvas[x1: x2, y1: y2] = color_or_image

  def update(self):
    self._display()
    now = time.time()
    self.delta = now - self._time
    self._time = now
    self._clock.tick(self._fps)
    self._events()

  def close(self):
    self.running = False
    pygame.quit()

  def title(self, text):
    pygame.display.set_caption(text)

  def _image(self, name, size=None):
    key = (name, size)
    if key not in self._images:
      path = pathlib.Path(__file__).parent / name
      image = imageio.imread(path)
      if size:
        image = np.array(Image.fromarray(image).resize(size))
      image = np.transpose(image, (1, 0, 2))[:, ::-1, :] / 255
      self._images[key] = image
    return self._images[key]

  def _display(self):
    canvas = (255 * self._canvas).astype(np.uint8)[:, ::-1]
    surface = pygame.surfarray.make_surface(canvas)
    self._screen.blit(surface, (0, 0))
    pygame.display.flip()
    self._canvas[:] = 0.0

  def _events(self):
    self._pressed = pygame.key.get_pressed()
    self._keydowns = []
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.KEYDOWN:
        self._keydowns.append(event.key)