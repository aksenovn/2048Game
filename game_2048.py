import random
import os

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.score = 0
        self.game_over = False
        self._add_random_tile()
        self._add_random_tile()

    def _add_random_tile(self):
        empty_cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    empty_cells.append((r, c))

        if empty_cells:
            r, c = random.choice(empty_cells)
            self.board[r][c] = 2 if random.random() < 0.9 else 4

    def display_board(self):
        os.system('cls' if os.name == 'nt' else 'clear') # Clear console
        print("-" * (self.size * 6 + 1))
        for row in self.board:
            print("|", end="")
            for tile in row:
                print(f"{tile:^5}|", end="")
            print("\n" + "-" * (self.size * 6 + 1))
        print(f"Score: {self.score}\n")

    def _get_empty_cells(self):
        empty_cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    empty_cells.append((r, c))
        return empty_cells

    def _has_moves(self):
        # Check for empty cells
        if self._get_empty_cells():
            return True

        # Check for possible merges horizontally and vertically
        for r in range(self.size):
            for c in range(self.size):
                if c < self.size - 1 and self.board[r][c] == self.board[r][c+1]:
                    return True
                if r < self.size - 1 and self.board[r][c] == self.board[r+1][c]:
                    return True
        return False

    def move(self, direction):
        if self.game_over:
            return False

        moved = False
        # Create a copy of the board to check if any move actually happened
        original_board = [row[:] for row in self.board]

        if direction == 'up':
            for c in range(self.size):
                column = [self.board[r][c] for r in range(self.size)]
                new_column, score_gained = self._slide_and_merge(column)
                for r in range(self.size):
                    self.board[r][c] = new_column[r]
                self.score += score_gained
        elif direction == 'down':
            for c in range(self.size):
                column = [self.board[r][c] for r in range(self.size)]
                new_column, score_gained = self._slide_and_merge(column[::-1])
                for r in range(self.size):
                    self.board[r][c] = new_column[::-1][r]
                self.score += score_gained
        elif direction == 'left':
            for r in range(self.size):
                row = self.board[r]
                new_row, score_gained = self._slide_and_merge(row)
                self.board[r] = new_row
                self.score += score_gained
        elif direction == 'right':
            for r in range(self.size):
                row = self.board[r]
                new_row, score_gained = self._slide_and_merge(row[::-1])
                self.board[r] = new_row[::-1]
                self.score += score_gained

        if original_board != self.board:
            moved = True
            self._add_random_tile()
            if not self._has_moves():
                self.game_over = True
        return moved

    def _slide_and_merge(self, line):
        # Remove zeros
        new_line = [tile for tile in line if tile != 0]
        score_gained = 0

        # Merge
        i = 0
        while i < len(new_line) - 1:
            if new_line[i] == new_line[i+1]:
                new_line[i] *= 2
                score_gained += new_line[i]
                new_line.pop(i+1)
            i += 1

        # Add zeros back
        new_line.extend([0] * (self.size - len(new_line)))
        return new_line, score_gained

    def check_game_over(self):
        return self.game_over


def main():
    game = Game2048()
    while not game.game_over:
        game.display_board()
        move = input("Enter move (w/a/s/d for up/left/down/right): ").lower()
        if move in ['w', 'a', 's', 'd']:
            direction_map = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}
            game.move(direction_map[move])
        else:
            print("Invalid move. Use w, a, s, or d.")
            input("Press Enter to continue...") # Pause to read message
    game.display_board()
    print("Game Over!")

if __name__ == "__main__":
    main()
