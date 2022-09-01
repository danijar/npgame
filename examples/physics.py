import npgame
import numpy as np
import pymunk


space = pymunk.Space()
space.gravity = (0, -9.81)


class Player:

  def __init__(self, x, y):
    self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    self.body.position = (x, y)
    shape = pymunk.Poly.create_box(size=(1, 1))
    shape.mass = 10
    space.add(body, shape)


EXAMPLE = """
####################
#                  #
#                * #
#                  #
#        ###   #   #
# ###          #   #
#         P    #  ##
#     ##      ##  ##
#   #####    #######
####################
"""


level = np.array(tuple(zip(*EXAMPLE.split('\n')[1:-1])))[:, ::-1]
player = None
for pos, char in np.ndenumerate(level):
  if char == 'P':
    player = Player(*pos)
  if char == '#':
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (x, y)
    shape = pymunk.Poly.create_box(size=(1, 1))
    space.add(body, shape)
won = False

game = npgame.Game(level.shape, scale=40)
game.title('Jumper')
while game.running:
  game.update()

  if game.pressed('escape'):
    game.close()

  if level[round(player[0]), round(player[1])] == '*' and not won:
    print('You Win!')
    won = True

  on_ground = (
      (level[int(player[0] + 0.0), int(player[1] - 0.1)] == '#') or
      (level[int(player[0] + 1.0), int(player[1] - 0.1)] == '#'))
  if on_ground:
    vel = [0, 0]
    if game.pressed('a'):
      vel[0] = -5
    if game.pressed('d'):
      vel[0] = +5
    if game.pressed('space'):
      vel[1] = +10
  else:
    vel[1] -= 20 * game.delta
  player = move(player, (vel[0] * game.delta, vel[1] * game.delta))

  game.draw(0, 0, *level.shape, [1, 1, 1])
  for (pos, char) in np.ndenumerate(level):
    if char == '#':
      game.draw(*pos, 1, 1, [0, 0, 0])
    if char == '*':
      game.draw(*pos, 1, 1, [1, 0.7, 0])
  game.draw(*player, 1, 1, [0, 0.5, 0])
