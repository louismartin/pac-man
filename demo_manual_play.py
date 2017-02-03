from pacman.agents import Ghost, PacMan
from pacman.board import Board, Candy
from pacman.game import Game, Action


board = Board('boards/simple_board.txt')
game = Game(board)

# Add agents to the game
game.add("PacMan", position=(5, 5))
game.add("Ghost", position=(0, 0))
game.add("Ghost", position=(0, 5))
game.add("Candy", position=(5, 3))


actions = {'w': Action.UP, 's': Action.DOWN,
           'a': Action.LEFT, 'd': Action.RIGHT}
cum_reward = 0
board_title = 'Reward : {}'.format(cum_reward)
game.draw_state(board_title)
while not game.finished:
    action_char = input('Move with: a,w,d,s + enter')
    if action_char in actions.keys():
        action = actions[action_char]
        # Compute next moves
        reward = game.play(action)
        cum_reward += reward

        board_title = 'Reward : {}'.format(cum_reward)
        game.draw_state(board_title)
    else:
        print('Key %s not valid' % action_char)

#total_reward = game.play_game()
#print('Game finished !\nTotal_reward : {reward}'.format(reward=total_reward))
