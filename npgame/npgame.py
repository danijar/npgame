import time
import pathlib

import imageio
import numpy as np
import pygame
from PIL import Image, ImageFont, ImageDraw


class Game:

  def __init__(self, grid=(40, 30), scale=20, fps=60):
    pygame.init()
    self.running = True
    self.delta = 0
    self.resize(grid, scale)
    self._images = {}
    self._texts = {}
    self._fonts = {}
    self._pressed = None
    self._keydowns = None
    self._fps = fps
    self._clock = pygame.time.Clock()
    self._time = time.time()

  def resize(self, grid=None, scale=None):
    self._grid = grid or self._grid
    self._scale = scale or self._scale
    self._canvas = np.zeros(
        (int(grid[0] * scale), int(grid[1] * scale), 3), np.float32)
    self._screen = pygame.display.set_mode(self._canvas.shape[:2])

  def pressed(self, key):
    if not self._pressed:
      return False
    code = pygame.key.key_code(key)
    return self._pressed[code] or code in self._keydowns

  def draw(self, x, y, w, h, color=None, array=None, image=None):
    if sum(x is not None for x in (color, array, image)) != 1:
      raise ValueError('Provide exactly one of color, array, or image.')
    x, y = int(x * self._scale), int(y * self._scale)
    w, h = int(w * self._scale), int(h * self._scale)
    x1, x2, y1, y2 = x, x + w, y, y + h
    x1, x2 = max(0, x1), min(x2, self._canvas.shape[0])
    y1, y2 = max(0, y1), min(y2, self._canvas.shape[1])
    if x2 - x1 < 1 or y2 - y1 < 1:
      return
    if color is not None:
      color = np.asarray(color, np.float32)
      assert color.shape in ((1,), (3,), (4,)), color.shape
      content = color[None, None, :]
    if array is not None:
      array = np.asarray(array, np.float32)
      assert len(array.shape) == 3
      assert array.shape[-1] in (1, 3, 4), image.shape
      if array.shape[:2] != (w, h):
        array = (255 * array).astype(np.uint8)
        array = np.asarray(Image.fromarray(array).resize((w, h))) / 255
      content = array[x1 - x: x2 - x, y1 - y: y2 - y]
    if image is not None:
      image = self._image(image, (w, h))
      assert len(image.shape) == 3
      assert image.shape[-1] in (1, 3, 4), image.shape
      content = image[x1 - x: x2 - x, y1 - y: y2 - y]
    if content.shape[-1] in (1, 3):
      self._canvas[x1: x2, y1: y2] = content
    if content.shape[-1] == 4:
      bg = self._canvas[x1: x2, y1: y2]
      content, alpha = content[..., :3], content[..., -1:]
      self._canvas[x1: x2, y1: y2] = alpha * content + (1 - alpha) * bg

  def text(self, x, y, message, font, color=(0.5, 0.5, 0.5, 1.0), size=1):
    font = str(font)
    color = tuple(int(255 * x) for x in color)
    color = color + (255,) if len(color) == 3 else color
    assert len(color) == 4
    size = int(size * self._scale)
    key = (message, font, color, size)
    if key not in self._texts:
      if (font, size) not in self._fonts:
        if font == 'default':
          self._fonts[(font, size)] = ImageFont.load_default()
        else:
          assert font.endswith('.ttf'), font
          self._fonts[(font, size)] = ImageFont.truetype(font, size)
      font = self._fonts[(font, size)]
      w, h = font.getsize(message)
      image = Image.new('RGBA', (w, h), (255, 255, 255, 0))
      draw = ImageDraw.Draw(image)
      draw.text((0, 0), message, color, font)
      self._texts[key] = np.array(image).transpose((1, 0, 2))[:, ::-1, :] / 255
    array = self._texts[key]
    w, h = array.shape[:2]
    self.draw(x, y, w / self._scale, h / self._scale, array=array)

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
      if len(image.shape) == 2:
        image = image[..., None]
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
