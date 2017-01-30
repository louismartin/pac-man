import pytest
from pacman.board import Node


def test_pacman_initialized_at_zero(pacman):
    assert pacman.reward == 0


def test_pacman_move(node, pacman):
    pacman.move(node)
    assert(pacman.current_node.position == node.position)


@pytest.fixture
def pacman():
    from pacman.board import Node
    from pacman.agents import PacMan
    node = Node((0, 0))
    pacman = PacMan(node)
    return pacman


@pytest.fixture
def node():
    from pacman.board import Node
    position = (1, 2)
    return Node(position)
