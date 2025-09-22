# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification on Canvas

import sys

class CommandInterface:
    # The following is already defined and does not need modification
    # However, you may change or add to this code as you see fit, e.g. adding class variables to init

    def __init__(self):
        # Define the string to function command mapping
        self.command_dict = {
            "help" : self.help,
            "init_game" : self.init_game,
            "legal" : self.legal,
            "play" : self.play,
            "genmove" : self.genmove,
            "undo" : self.undo,
            "score" : self.score,
            "winner" : self.winner,
            "show" : self.show,
        }

    # Convert a raw string to a command and a list of arguments
    def process_command(self, string):
        string = string.lower().strip()
        command = string.split(" ")[0]
        args = [x for x in string.split(" ")[1:] if len(x) > 0]
        if command not in self.command_dict:
            print("? Uknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            print("Command '" + string + "' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False
        
    # Will continuously receive and execute commands
    # Commands should return True on success, and False on failure
    # Commands will automatically print '= 1' at the end of execution on success
    def main_loop(self):
        while True:
            string = input()
            if string.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(string):
                print("= 1\n")

    # List available commands
    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    #======================================================================================
    # End of predefined functionality. You will need to implement the following functions.
    # Arguments are given as a list of strings
    # We will only test error handling of the play command
    #======================================================================================

    def init_game(self, args):
        '''
            >> init_game <num_cols> <num_rows> <handicap> <score_cutoff>
            Initializes the game board with the dimension (<num_cols>, <num_rows>).
            Sets the handicap for the second player as <handicap>.
            Sets the winning score as <score_cutoff>.
        '''
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def legal(self, args):
        '''
            >> legal <col> <row>
            Checks if the current player can play at position (<col>, <row>) on the board.
        '''
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def play(self, args):
        '''
            >> play <col> <row>
            Places the current player's piece at position (<col>, <row>). Check if the move is legal before playing it.
        '''
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def genmove(self, args):
        '''
            >> genmove
            Generates and plays a random valid move.
        '''
        raise NotImplementedError("This command is not yet implemented.")
        return True

    def undo(self, args):
        '''
            >> undo
            Undoes the last move.
        '''
        raise NotImplementedError("This command is not yet implemented.")
        return True

    def score(self, args):
        '''
            >> score
            Prints the scores.
        '''
        raise NotImplementedError("This command is not yet implemented.")
        return True

    def winner(self, args):
        '''
            >> winner
            Prints the winner information.
        '''
        raise NotImplementedError("This command is not yet implemented.")
        return True

    def show(self, args):
        '''
            >> show
            Shows the game board.
        '''
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    #======================================================================================
    # End of functions requiring implementation
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()
