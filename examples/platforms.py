import npgame
import numpy as np


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
    player = pos
vel = [0, 0]
won = False

game = npgame.Game(level.shape, scale=40)
while game.running:
  game.update()

  def move(pos, vel, steps=20):
    for m in np.linspace(1.0, 0, steps):
      x = pos[0] + m * vel[0]
      y = pos[1]
      collision = (
          (level[int(x + 0), int(y + 0)] == '#') or
          (level[int(x + 1), int(y + 0)] == '#') or
          (level[int(x + 0), int(y + 1)] == '#') or
          (level[int(x + 1), int(y + 1)] == '#'))
      if not collision:
        break
    for m in np.linspace(1.0, 0, steps):
      y = pos[1] + m * vel[1]
      collision = (
          (level[int(x + 0), int(y + 0)] == '#') or
          (level[int(x + 1), int(y + 0)] == '#') or
          (level[int(x + 0), int(y + 1)] == '#') or
          (level[int(x + 1), int(y + 1)] == '#'))
      if not collision:
        break
    return (x, y)

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
