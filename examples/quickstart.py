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
