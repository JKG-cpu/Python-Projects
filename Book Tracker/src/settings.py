import json
import time

from VividText import VividText as vt
from os.path import join
from os import system, name

# Variables
mPrinter = vt(bold=True, sleep=.03)
pPrinter = vt(bold=True, sleep=0)

# Functions
def cc():
    system("cls" if name == "nt" else "clear")

# Classes
class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
        
        except Exception as e:
            raise ValueError("Error loading data: {e}")

        return data

    def save_data(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent = 2)

class InputParser:
    def parse_command(self, tokens) -> tuple:
        fixed_input = []
        inside_quotes = False
        buffer = []

        for token in tokens:
            if token.startswith('"') and token.endswith('"'):
                fixed_input.append(token)
            elif token.startswith('"'):
                inside_quotes = True
                buffer.append(token)
            elif token.endswith('"') and inside_quotes:
                # end of a quoted phrase
                buffer.append(token)
                fixed_input.append(' '.join(buffer))
                buffer = []
                inside_quotes = False
            elif inside_quotes:
                # middle of a quoted phrase
                buffer.append(token)
            else:
                # normal token
                fixed_input.append(token)
        
        marked_tokens = []

        for token in fixed_input:
            # Base commands
            if token.startswith('-a'):
                marked_tokens.append((token, 'add'))

            elif token.startswith('-h'):
                marked_tokens.append((token, 'help'))

            elif token.startswith("-v"):
                marked_tokens.append((token, "view"))

            elif token.startswith("-q"):
                marked_tokens.append((token, 'quit'))

            # Others
            elif token.startswith('"') or token.startswith("'"):
                marked_tokens.append((token, 'value'))
            
            elif token.startswith("-"):
                marked_tokens.append((token, "flag"))

            else:
                marked_tokens.append((token, 'invalid'))

        return (fixed_input, marked_tokens)

    def command_input(self, message: str = "Enter a command or type -help for help"):
        while True:
            raw_input = mPrinter.inputTypewriter(message)
            fixed_input, markdowns = self.parse_command(raw_input.strip().split())

            valid_command = True

            for _, ttype in markdowns:
                if ttype == "invalid":
                    valid_command = False
                    break
            
            if valid_command:
                break
                
            else:
                mPrinter.typewriter("That is not a valid command.")
                mPrinter.inputTypewriter("Press Enter to continue.", end=' ')
                cc()
                continue
        
        return fixed_input, markdowns

