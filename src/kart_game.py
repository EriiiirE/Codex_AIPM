"""Terminal kart racing demo using only the Python standard library.

Controls:
    W - Accelerate
    S - Brake
    A - Move left
    D - Move right

Run the game with `python src/kart_game.py`. Use `--test` to run a short
non-interactive session for automated checks.
"""

import argparse
import random
import time


WIDTH = 20  # track width (columns)
HEIGHT = 10  # visible rows

# ANSI color helpers
RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
GREY_BG = "\033[47m"


def clear() -> None:
    """Clear the terminal screen."""
    print("\033[H\033[J", end="")


def render(kart_x: int, obstacles: list[tuple[int, int]], clear_screen: bool = True) -> None:
    """Render the track, kart, trees, and rocks."""
    if clear_screen:
        clear()
    for y in range(HEIGHT):
        line = []
        for x in range(WIDTH):
            if x == 0 or x == WIDTH - 1:
                line.append(GREEN + "T" + RESET)  # trees at the sides
            else:
                cell = GREY_BG + " " + RESET  # road
                for ox, oy in obstacles:
                    if (ox, oy) == (x, y):
                        cell = RED + "O" + RESET  # rock obstacle
                if y == HEIGHT - 1 and x == kart_x:
                    cell = RED + "K" + RESET  # kart
                line.append(cell)
        print("".join(line))
    print("Use WASD then Enter to move, Q to quit")


def game(test_mode: bool = False) -> None:
    kart_x = WIDTH // 2
    speed = 0
    obstacles: list[tuple[int, int]] = []
    frame = 0
    commands = iter("wdwdss") if test_mode else None

    while True:
        render(kart_x, obstacles, clear_screen=not test_mode)

        if (kart_x, HEIGHT - 1) in obstacles:
            print("Crashed!")
            break

        if test_mode:
            try:
                cmd = next(commands)
            except StopIteration:
                break
        else:
            cmd = input().lower().strip()[:1]

        if cmd == "q":
            break
        if cmd == "w":
            speed = 1
        elif cmd == "s":
            speed = 0
        elif cmd == "a":
            kart_x = max(1, kart_x - 1)
        elif cmd == "d":
            kart_x = min(WIDTH - 2, kart_x + 1)

        # Move obstacles downward based on speed
        obstacles = [(x, y + speed) for x, y in obstacles if y + speed < HEIGHT]

        # Add a new obstacle every few frames
        if frame % 3 == 0:
            obstacles.append((random.randint(1, WIDTH - 2), 0))
        frame += 1
        time.sleep(0.2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple terminal kart game")
    parser.add_argument("--test", action="store_true", help="Run short automated test")
    args = parser.parse_args()
    game(test_mode=args.test)

