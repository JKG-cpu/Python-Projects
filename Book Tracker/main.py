from src.settings import *
from src.tasks import *

class Main:
    def __init__(self):
        # Class functions
        self.taskManager = Manager(join("src", "database", "tasks.json"))
        self.inputParser = InputParser()

    # CMD Line functions
    def help(self):
        # Print all the commands for base out
        # Allow user to view "details" on a command
        pass

    def add_task(self):
        # Have the user add tasks
        pass

    def view_tasks(self):
        # Have the user view tasks
        pass

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
                        self.add_task()

                    # Check if view task
                    elif ttype == "view":
                        self.view_tasks()

                    # Check if -help
                    elif ttype == "help":
                        self.help()

                    else:
                        pass

if __name__ == '__main__':
    main = Main()
    main.main()