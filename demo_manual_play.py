from pacman.agents import Ghost, PacMan
from pacman.board import Board, Candy
from pacman.game import Game, Action


board = Board('boards/simple_board.txt')
game = Game(board)

# Create agents and add them to game
pacman_init_node = board.nodes[(5, 5)]
pacman = PacMan(pacman_init_node)
game.add_pacman(pacman)

ghost1_init_node = board.nodes[(0, 0)]
ghost1 = Ghost(ghost1_init_node)
game.add_ghost(ghost1)

ghost2_init_node = board.nodes[(0, 5)]
ghost2 = Ghost(ghost2_init_node)
game.add_ghost(ghost2)

candy1_node = board.nodes[(5, 3)]
candy1 = Candy(candy1_node)
game.add_candy(candy1)


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
