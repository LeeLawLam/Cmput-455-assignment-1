# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification on Canvas

import sys
import random
from typing import List, Tuple, Optional, Set

class CommandInterface:
    # The following is already defined and does not need modification
    # However, you may change or add to this code as you see fit, e.g. adding class variables to init

    def __init__(self):
        # Define the string to function command mapping
        self.command_dict = {
            "help": self.help,
            "init_game": self.init_game,
            "legal": self.legal,
            "play": self.play,
            "genmove": self.genmove,
            "undo": self.undo,
            "score": self.score,
            "winner": self.winner,
            "show": self.show,
        }
        # Game state (initialized by init_game)
        self.cols: int = 0
        self.rows: int = 0
        self.cutoff: float = 0.0
        self.handicap: float = 0.0
        self.board: List[List[int]] = []           # board[row][col] in {0,1,2}
        self.current: int = 1                      # 1 or 2
        self.history: List[Tuple[int, int, int]] = []  # (c, r, player)
        self.ended: bool = False
        
    # Convert a raw string to a command and a list of arguments
    def process_command(self, string: str) -> bool:
        string = string.strip()
        if not string:
            print("= -1\n")
            return False

        # Split safely (command plus args). Be forgiving about extra spaces.
        parts = string.split()
        command = parts[0].lower()
        args = parts[1:]

        if command not in self.command_dict:
            print("? Unknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            # Never crash; report failure status
            print(f"Command '{string}' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False
        
    # Will continuously receive and execute commands
    # Commands should return True on success, and False on failure
    # Commands will automatically print '= 1' at the end of execution on success
    def main_loop(self):
        while True:
            line = input()
            if not line:
                # treat empty line as failure
                print("= -1\n")
                continue
            if line.split()[0].lower() == "exit":
                print("= 1\n")
                return True
            if self.process_command(line):
                # Success status line is printed here
                print("= 1\n")

    # List available commands
    def help(self, args: List[str]) -> bool:
        for cmd in self.command_dict:
            if cmd != "help":
                print(cmd)
        print("exit")
        return True


    #======================================================================================
    # End of predefined functionality. You will need to implement the following functions.
    # Arguments are given as a list of strings
    # We will only test error handling of the play command
    #======================================================================================

    def init_game(self, args: List[str]) -> bool:
        '''
            >> init_game <num_cols> <num_rows> <handicap> <score_cutoff>
            Initializes the game board with the dimension (<num_cols>, <num_rows>).
            Sets the handicap for the second player as <handicap>.
            Sets the winning score as <score_cutoff>.
        '''
        if len(args) != 4:
            print("= -1\n")
            return False
        try:
            w = int(args[0])
            h = int(args[1])
            p = float(args[2])   # handicap
            s = float(args[3])   # cutoff (0.0 => infinite)
        except ValueError:
            print("= -1\n")
            return False

        if not (1 <= w <= 20 and 1 <= h <= 20):
            print("= -1\n")
            return False
        if s < 0:
            print("= -1\n")
            return False

        self.cols = w
        self.rows = h
        self.handicap = p
        self.cutoff = s
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current = 1
        self.history.clear()
        self.ended = False
        return True

    def legal(self, args: List[str]) -> bool:
        '''
            >> legal <col> <row>
            Checks if the current player can play at position (<col>, <row>) on the board.
        '''
        if len(args) != 2:
            print("= -1\n")
            return False
        try:
            c = int(args[0])
            r = int(args[1])
        except ValueError:
            print("= -1\n")
            return False

        print("yes" if self._is_legal(c, r) else "no")
        return True

    def play(self, args: List[str]) -> bool:
        '''
            >> play <col> <row>
            Places the current player's piece at position (<col>, <row>). Check if the move is legal before playing it.
        '''
        if len(args) != 2:
            print("= -1\n")
            return False
        try:
            c = int(args[0])
            r = int(args[1])
        except ValueError:
            print("= -1\n")
            return False

        if not self._is_legal(c, r):
            print("= -1\n")
            return False

        # Apply move
        self.board[r][c] = self.current
        self.history.append((c, r, self.current))

        # Check end conditions
        p1, p2 = self._compute_scores()
        if self._game_should_end_after_move(p1, p2):
            self.ended = True
        else:
            self.current = 3 - self.current
        return True

    def genmove(self, args: List[str]) -> bool:
        '''
            >> genmove
            Generates and plays a random valid move.
        '''
        moves = [(c, r)
                 for r in range(self.rows)
                 for c in range(self.cols)
                 if self._is_legal(c, r)]
        if not moves:
            print("resign")
            return True  # success status with "resign" text
        c, r = random.choice(moves)

        # play it (same as play, but we already know it's legal)
        self.board[r][c] = self.current
        self.history.append((c, r, self.current))
        print(f"{c} {r}")

        p1, p2 = self._compute_scores()
        if self._game_should_end_after_move(p1, p2):
            self.ended = True
        else:
            self.current = 3 - self.current
        return True

    def undo(self, args: List[str]) -> bool:
        '''
            >> undo
            Undoes the last move.
        '''
        if args:
            # No args expected
            print("= -1\n")
            return False
        if not self.history:
            print("= -1\n")
            return False
        c, r, player = self.history.pop()
        self.board[r][c] = 0
        self.current = player
        self.ended = False
        return True

    def score(self, args: List[str]) -> bool:
        '''
            >> score
            Prints the scores.
        '''
        p1, p2 = self._compute_scores()
        def fmt(x: float) -> str:
            xi = int(round(x))
            return str(xi) if abs(x - xi) < 1e-9 else str(x)
        print(f"{fmt(p1)} {fmt(p2)}")
        return True

    def winner(self, args: List[str]) -> bool:
        '''
            >> winner
            Prints the winner information.
        '''
        p1, p2 = self._compute_scores()
        w = self._winner_from_scores(p1, p2)
        print(w)
        return True

    def show(self, args: List[str]) -> bool:
        '''
            >> show
            Shows the game board.
        '''
        trail = " "
        for r in range(self.rows):
            row_syms = []
            for c in range(self.cols):
                v = self.board[r][c]
                row_syms.append('_' if v == 0 else str(v))
            print(' '.join(row_syms) + trail)
        return True

    def _in_bounds(self, c: int, r: int) -> bool:
        return 0 <= c < self.cols and 0 <= r < self.rows

    def _is_legal(self, c: int, r: int) -> bool:
        return (not self.ended) and self._in_bounds(c, r) and self.board[r][c] == 0

    def _compute_scores(self) -> Tuple[float, float]:
        """Compute scores from maximal lines in 4 directions, then +1 for stones
        not in any length>=2 line; add handicap to player 2."""
        s1 = 0
        s2 = 0

        # Track cells that belong to any L>=2 line (for either player)
        in_long_line: Set[Tuple[int, int]] = set()

        # Directions: E, S, SE, NE
        dirs = [(1, 0), (0, 1), (1, 1), (1, -1)]

        # Count maximal runs with L >= 2
        for r in range(self.rows):
            for c in range(self.cols):
                p = self.board[r][c]
                if p == 0:
                    continue
                for dc, dr in dirs:
                    pc, pr = c - dc, r - dr
                    # Only start counting if (c,r) is the start of a run in this direction
                    if self._in_bounds(pc, pr) and self.board[pr][pc] == p:
                        continue
                    # Walk forward
                    cc, rr = c, r
                    length = 0
                    while self._in_bounds(cc, rr) and self.board[rr][cc] == p:
                        length += 1
                        cc += dc
                        rr += dr
                    if length >= 2:
                        val = 1 << (length - 1)  # 2^(L-1)
                        if p == 1:
                            s1 += val
                        else:
                            s2 += val
                        # Mark every cell in this long line segment
                        cc2, rr2 = c, r
                        for _ in range(length):
                            in_long_line.add((cc2, rr2))
                            cc2 += dc
                            rr2 += dr

        # Now count singletons (+1) for stones not in any long line
        for r in range(self.rows):
            for c in range(self.cols):
                p = self.board[r][c]
                if p == 0:
                    continue
                if (c, r) not in in_long_line:
                    if p == 1:
                        s1 += 1
                    else:
                        s2 += 1

        # Apply handicap to player 2
        s2 += self.handicap
        return float(s1), float(s2)

    def _board_full(self) -> bool:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 0:
                    return False
        return True

    def _game_should_end_after_move(self, s1: float, s2: float) -> bool:
        # cutoff == 0 → no winner until board is full
        if self.cutoff == 0.0:
            return self._board_full()
        # cutoff > 0 → someone winning immediately ends the game
        if s1 >= self.cutoff or s2 >= self.cutoff:
            return True
        return False

    def _winner_from_scores(self, s1: float, s2: float) -> str:
        # cutoff == 0: only decide when board is full
        if self.cutoff == 0.0:
            if not self._board_full():
                return "unknown"
            # Board full: higher score wins; tie -> unknown
            if s1 > s2:
                return "1"
            if s2 > s1:
                return "2"
            return "unknown"

        # cutoff > 0: if one or both reached cutoff, higher score wins; tie -> unknown
        if s1 >= self.cutoff or s2 >= self.cutoff:
            if s1 > s2:
                return "1"
            if s2 > s1:
                return "2"
            return "unknown"

        return "unknown"
    
    #======================================================================================
    # End of functions requiring implementation
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()
