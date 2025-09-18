"""终端版 2048 游戏，使用 Mac 键盘方向键控制。

运行方式：在支持 curses 的终端（macOS Terminal / iTerm2 等）中执行

    python hello.py

方向键控制滑动，合并相同数字。按 `q` 退出，`r` 在结束后重新开始。
"""

from __future__ import annotations

import curses
import random
from dataclasses import dataclass, field
from typing import List, Tuple


Board = List[List[int]]
Direction = str


@dataclass
class Game2048:
    size: int = 4
    board: Board = field(default_factory=list)
    score: int = 0

    def __post_init__(self) -> None:
        if not self.board:
            self.board = [[0] * self.size for _ in range(self.size)]
        self._spawn_tile()
        self._spawn_tile()

    def move(self, direction: Direction) -> bool:
        moved = False
        if direction in ("left", "right"):
            for y in range(self.size):
                row = self.board[y][:]
                if direction == "right":
                    row.reverse()
                collapsed, gained = self._collapse_line(row)
                if direction == "right":
                    collapsed.reverse()
                if self.board[y] != collapsed:
                    moved = True
                    self.board[y] = collapsed
                    self.score += gained
        elif direction in ("up", "down"):
            for x in range(self.size):
                column = [self.board[y][x] for y in range(self.size)]
                if direction == "down":
                    column.reverse()
                collapsed, gained = self._collapse_line(column)
                if direction == "down":
                    collapsed.reverse()
                if [self.board[y][x] for y in range(self.size)] != collapsed:
                    moved = True
                    for y in range(self.size):
                        self.board[y][x] = collapsed[y]
                    self.score += gained
        else:
            return False

        if moved:
            self._spawn_tile()
        return moved

    def has_moves(self) -> bool:
        if any(0 in row for row in self.board):
            return True
        for y in range(self.size):
            for x in range(self.size - 1):
                if self.board[y][x] == self.board[y][x + 1]:
                    return True
        for x in range(self.size):
            for y in range(self.size - 1):
                if self.board[y][x] == self.board[y + 1][x]:
                    return True
        return False

    def _collapse_line(self, line: List[int]) -> Tuple[List[int], int]:
        tight = [value for value in line if value]
        merged: List[int] = []
        gained = 0
        skip = False
        for idx, value in enumerate(tight):
            if skip:
                skip = False
                continue
            if idx + 1 < len(tight) and tight[idx + 1] == value:
                new_value = value * 2
                merged.append(new_value)
                gained += new_value
                skip = True
            else:
                merged.append(value)
        merged.extend([0] * (self.size - len(merged)))
        return merged, gained

    def _spawn_tile(self) -> None:
        empties = [(y, x) for y in range(self.size) for x in range(self.size) if self.board[y][x] == 0]
        if not empties:
            return
        y, x = random.choice(empties)
        self.board[y][x] = 4 if random.random() < 0.1 else 2


def draw_board(stdscr: "curses._CursesWindow", game: Game2048, message: str = "") -> None:
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    info_lines = ["2048 — 使用方向键，按 q 退出。", f"分数：{game.score}"]

    cell_width = 6
    board_width = game.size * cell_width + 1
    start_x = max(0, (width - board_width) // 2)
    start_y = max(0, (height - (game.size * 2 + len(info_lines) + 1)) // 2)

    for idx, line in enumerate(info_lines):
        stdscr.addstr(start_y + idx, start_x, line)

    grid_top = start_y + len(info_lines) + 1
    horizontal = "+" + "+".join(["-" * (cell_width - 1)] * game.size) + "+"
    for row_idx, row in enumerate(game.board):
        y = grid_top + row_idx * 2
        stdscr.addstr(y, start_x, horizontal)
        row_line = "|".join(f"{value or '':^{cell_width - 1}}" for value in row)
        stdscr.addstr(y + 1, start_x, "|" + row_line + "|")
    stdscr.addstr(grid_top + game.size * 2, start_x, horizontal)

    if message:
        stdscr.addstr(grid_top + game.size * 2 + 2, start_x, message)

    stdscr.refresh()


def game_loop(stdscr: "curses._CursesWindow") -> None:
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    game = Game2048()
    message = ""

    while True:
        draw_board(stdscr, game, message)
        if not game.has_moves():
            draw_board(stdscr, game, "游戏结束！按 q 退出，按 r 重新开始。")
            key = stdscr.getch()
            if key in (ord("q"), ord("Q")):
                break
            if key in (ord("r"), ord("R")):
                game = Game2048()
                message = ""
                continue
            continue

        key = stdscr.getch()
        if key in (ord("q"), ord("Q")):
            break

        direction: Direction | None = None
        if key == curses.KEY_UP:
            direction = "up"
        elif key == curses.KEY_DOWN:
            direction = "down"
        elif key == curses.KEY_LEFT:
            direction = "left"
        elif key == curses.KEY_RIGHT:
            direction = "right"

        if direction:
            if not game.move(direction):
                message = "该方向不能移动，换一个方向试试。"
            else:
                message = ""
        else:
            message = "请使用方向键，按 q 退出。"


def main() -> None:
    try:
        curses.wrapper(game_loop)
    except curses.error:
        print("终端窗口太小，无法显示游戏，请放大后重试。")


if __name__ == "__main__":
    main()
