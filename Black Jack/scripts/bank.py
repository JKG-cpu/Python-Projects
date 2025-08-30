from VividText import VividText as vt
import json
from os.path import join
from time import sleep
from random import uniform, randint 

from .utils import cc

class Bank:
    def __init__(self, tp=vt(bold=True, sleep=.03), file_path=join("..", "database", "bank.json")):
        #* Init TP
        self.tp = tp

        #* Get Balance
        self.data_fp = file_path
        self.data = None
        self.load_data()

        #* Menu Options
        self.options = ['Withdraw Money', "Deposit Money", "View Balance", "Exit"]

    #* Load Data
    def load_data(self):
        with open(self.data_fp, 'r') as data:
            self.data = json.load(data)
    
    #* Save Data
    def save_data(self):
        print(self.data)
        with open(self.data_fp, 'w') as data:
            json.dump(self.data, data, indent=2)

    #* Get the player's pocket amount
    def get_pocket_amount(self):
        return self.data['pocket-balance']
    
    def loading_bar(self):
        length = 25
        min_delay = 0.05
        max_delay = 0.1
        progress = 0

        while progress < 100:
            filled = int((progress / 100) * length)

            # ANSI: bold green bar + bold white percent
            bar = f"\033[1;32m[{'#' * filled}{' ' * (length - filled)}]\033[1;37m {progress:>3}%\033[0m"
            print("\r" + bar, end="", flush=True)

            if progress >= 90:
                sleep(uniform(max_delay * 1.5, max_delay * 2.5))
                progress += randint(1, 2)
            else:
                sleep(uniform(min_delay, max_delay))
                progress += randint(1, 3)

        # Final bar
        final = f"\033[1;32m[{'#' * length}]\033[1;37m 100%\033[0m"
        print("\r" + final)

    def dep_money(self):
        cc()
        bank_balance = self.data['bank-balance']
        pocket_balance = self.data['pocket-balance']

        if pocket_balance == 0:
            self.tp.typewriter("You have no money in your wallet!")
            return

        run = True
        while run:
            self.tp.typewriter(f"Amount in Bank: ${bank_balance:.2f}")
            self.tp.typewriter(f"Amount in wallet: ${pocket_balance:.2f}")

            print()

            amount_to_deposit = self.tp.inputTypewriter("Select an amount of cash you would like to deposit")

            if amount_to_deposit.isdigit():
                amount_to_deposit = round(int(amount_to_deposit), 2)
                if amount_to_deposit <= pocket_balance:
                    print()
                    self.tp.typewriter(f"[DEPOSIT] Depositing ${amount_to_deposit:.2f} from your wallet.")
                    self.loading_bar()

                    bank_balance += amount_to_deposit
                    pocket_balance -= amount_to_deposit

                    self.tp.typewriter("[TRANSACTION] Transaction Complete.")

                    run = False
                    continue
            
                else:
                    self.tp.typewriter("You don't have that much money in your wallet!")
            
            else:
                self.tp.typewriter("That is not a valid amount (Type x.xx).")
            
            self.tp.inputTypewriter("Press Enter to continue.")
            cc()
        
        self.data['bank-balance'] = bank_balance
        self.data['pocket-balance'] = pocket_balance
        self.save_data()

    def with_money(self):
        cc()
        bank_balance = self.data['bank-balance']
        pocket_balance = self.data['pocket-balance']

        if bank_balance == 0:
            self.tp.typewriter('You have no money in your bank account!')
            return
        
        run = True
        while run:
            self.tp.typewriter(f"Amount in Bank: ${bank_balance:.2f}")
            self.tp.typewriter(f"Amount in wallet: ${pocket_balance:.2f}")

            print()

            amount_to_withdraw = self.tp.inputTypewriter("Select an amount of cash you would like to withdraw")

            if amount_to_withdraw.isdigit():
                amount_to_withdraw = round(int(amount_to_withdraw), 2)
                if amount_to_withdraw <= bank_balance:
                    print()
                    self.tp.typewriter(f"[WITHDRAW] Withdrawing ${amount_to_withdraw:.2f} from your bank account.")
                    self.loading_bar()

                    bank_balance -= amount_to_withdraw
                    pocket_balance += amount_to_withdraw

                    self.tp.typewriter("[TRANSACTION] Transaction Complete.")

                    run = False
                    continue

                else:
                    self.tp.typewriter("You don't have that much money in your bank!")

            else:
                self.tp.typewriter("That is not a valid amount (Type x.xx).")

            self.tp.inputTypewriter("Press Enter to continue.")
            cc()
        
        self.data['bank-balance'] = bank_balance
        self.data['pocket-balance'] = pocket_balance
        self.save_data()

    def view(self):
        self.tp.typewriter(f"The amount of money in your wallet: {self.get_pocket_amount()}")
        self.tp.typewriter(f"The amount of money in your bank: {self.data['bank-balance']}")

    def main(self):
        run = True
        while run:
            self.tp.menuTypewriter(' | ', self.options)
            option = self.tp.inputTypewriter("Select an option").title()

            if option == 'Exit' or option.startswith("E"):
                run = False

            elif option == 'Deposit Money' or option.startswith("D"):
                self.dep_money()
                self.tp.inputTypewriter("Press Enter to continue.", end='')
                cc()

            elif option == 'Withdraw Money' or option.startswith("W"):
                self.with_money()
                self.tp.inputTypewriter("Press Enter to continue.", end='')
                cc()

            elif option == 'View Balance' or option.startswith("V"):
                self.view()
                self.tp.inputTypewriter("Press Enter to continue.", end='')
                cc()

            else:
                self.tp.typewriter("Not a valid option.")
                self.tp.inputTypewriter("Press Enter to continue.", end='')
                cc()

        cc()