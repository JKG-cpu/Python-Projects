from VividText import VividText as vt
from os.path import join

from scripts.utils import cc
from scripts import Bank, Game

class Menu:
    def __init__(self):
        #* Init TPs
        self.tp = vt(bold=True, sleep=.03)

        #* Menu Options
        self.menu_options = ['Casino', "Bank", "Quit"]

        self.bank = Bank(file_path=join('database', 'bank.json'))
        self.casino = Game(self.bank.get_pocket_amount())

    def run_casino(self):
        self.casino.main()
        self.bank.data['pocket-balance'] = self.casino.get_winnings()
        self.bank.save_data()

    def run_bank(self):
        self.bank.main()
        self.casino.reset_player_pocket(self.bank.get_pocket_amount())

    def main(self):
        run = True
        while run:
            self.tp.menuTypewriter(" | ", self.menu_options)
            print()
            choice = self.tp.inputTypewriter("Select an option").title()

            if choice.startswith("C"):
                self.run_casino()
            
            elif choice.startswith("B"):
                self.run_bank()
            
            elif choice.startswith("Q"):
                self.tp.slow_type("Quitting...", 'g', 10, .7, end='')
                run = False
                continue
        
            else:
                self.tp.typewriter("That is not a valid option.")
                self.tp.inputTypewriter("Press Enter to continue.", end=' ')
                cc()

        cc()

Menu().main()