import npgame

margin = 0.1
w = h = 1 - 2 * margin
countdown = 1
scale = 20

grid = (10, 20)
game = npgame.Game(grid, scale)
while game.running:
  if countdown <= 0:
    countdown = 1
    scale *= 1.1
    grid = (grid[1], grid[0])
    game.resize(grid, scale)
  game.update()
  if game.pressed('escape'):
    game.close()
  game.draw(0, 0, grid[0], grid[1], (1, 1, 1))
  for x in range(grid[0]):
    for y in range(grid[1]):
      game.draw(x + margin, y + margin, w, h, (0, 1, 0, 0.3))
  countdown -= game.delta
