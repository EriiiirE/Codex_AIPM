import curses
import random
import time

class SnakeGame:
    """Simple terminal-based Snake game using curses.

    Controls:
        Arrow keys: change direction
        q: quit the game
    """
    def __init__(self, height: int = 20, width: int = 60) -> None:
        self.height = height
        self.width = width
        # Initialize snake in the middle of the screen
        self.snake = [(height // 2, width // 2 + i) for i in range(3)]
        self.direction = curses.KEY_LEFT
        self.food = self._random_food()
        self.score = 0

    def _random_food(self) -> tuple[int, int]:
        """Return a random position for food that is not on the snake."""
        while True:
            position = (
                random.randint(1, self.height - 2),
                random.randint(1, self.width - 2),
            )
            if position not in self.snake:
                return position

    def run(self, stdscr: "curses._CursesWindow") -> None:
        """Main game loop."""
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.keypad(True)

        while True:
            key = stdscr.getch()
            if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                self.direction = key
            elif key == ord("q"):
                break

            head_y, head_x = self.snake[0]
            if self.direction == curses.KEY_UP:
                head_y -= 1
            elif self.direction == curses.KEY_DOWN:
                head_y += 1
            elif self.direction == curses.KEY_LEFT:
                head_x -= 1
            elif self.direction == curses.KEY_RIGHT:
                head_x += 1

            new_head = (head_y, head_x)
            # End game if hitting wall or itself
            if (
                head_y in [0, self.height - 1]
                or head_x in [0, self.width - 1]
                or new_head in self.snake
            ):
                break

            self.snake.insert(0, new_head)
            if new_head == self.food:
                self.score += 1
                self.food = self._random_food()
            else:
                self.snake.pop()

            stdscr.clear()
            self._draw_board(stdscr)
            stdscr.addstr(self.height, 0, f"Score: {self.score}    Quit: q")
            stdscr.refresh()
            time.sleep(0.1)

        stdscr.nodelay(False)
        stdscr.addstr(self.height // 2, self.width // 2 - 5, "Game Over")
        stdscr.refresh()
        stdscr.getch()

    def _draw_board(self, stdscr: "curses._CursesWindow") -> None:
        """Draw borders, food, and snake."""
        for y in range(self.height):
            stdscr.addch(y, 0, "#")
            stdscr.addch(y, self.width - 1, "#")
        for x in range(self.width):
            stdscr.addch(0, x, "#")
            stdscr.addch(self.height - 1, x, "#")
        stdscr.addch(self.food[0], self.food[1], "*")
        for y, x in self.snake:
            stdscr.addch(y, x, "O")


def main() -> None:
    """Entry point to launch the game."""
    curses.wrapper(SnakeGame().run)


if __name__ == "__main__":
    main()
