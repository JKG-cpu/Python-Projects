from src.settings import *
from src.tasks import *

class Main:
    def __init__(self):
        # Class functions
        self.bookManager = BookManager(join("src", "database", "tasks.json"))
        self.inputParser = InputParser()

    # CMD Line Functions
    def help(self):
        # Print all the commands for base out
        # Allow user to view "details" on a command
        pass

    def add_book(self):
        run = True
        while run:
            _, markdowns = self.inputParser.command_input(
                "Enter in book details"
            )
            markdowns = iter(markdowns)
            data = {}

            for item in markdowns:
                value, key = item
                if key == "flag":
                    value = value.strip("-")
                    next_item = next(markdowns, None)
                    if next_item:
                        data[value] = next_item[0]
            
            if (not data) or ("name" not in list(data.keys())):
                mPrinter.typewriter("Type -help for help on the book addition command.")

            else:
                self.bookManager.create_new_entry(
                    name = data["name"],
                    pages = data["pages"] if "pages" in list(data.keys()) else None,
                    goal = data["goal"] if "goal" in list(data.keys()) else None
                )
                run = False

    def view_books(self):
        self.bookManager.view_books()

    # Main Loop
    def main(self):
        run = True

        while run:
            fixed_input, markdowns = self.inputParser.command_input()

            # Check if quit
            has_quit = any(mark[1] == 'quit' for mark in markdowns)

            if has_quit:
                mPrinter.typewriter("Closing program...")
                time.sleep(.5)
                run = False
                cc()
                continue

            else:
                for _, ttype in markdowns:
                    # Check if add task
                    if ttype == "add":
                        self.add_book()

                    # Check if view task
                    elif ttype == "view":
                        self.view_books()

                    # Check if -help
                    elif ttype == "help":
                        self.help()

                    else:
                        pass

if __name__ == '__main__':
    main = Main()
    main.main()