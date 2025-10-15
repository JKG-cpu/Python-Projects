import json
from datetime import date
from VividText import VividText as vt

from .helper_functions import *

class Transactions:
    def __init__(self, data_fp: str):
        # Base Variables
        self.main_tp = vt(bold=True, sleep=.03)
        self.quick_tp = vt(bold=True, sleep=0)
        self.error_tp = vt(color="bright_red", bold=True, sleep=0)

        self.req_args = ["name", "amount"]
        self.other_args = ["date"]
        self.page_length = 10

        # Grab and load the data
        self.data_fp = data_fp
        self.data = self._load_data()

    # Data Handling Methods
    #region
    def _load_data(self) -> list | dict:
        data = []

        try:
            with open(self.data_fp, "r") as f:
                data = json.load(f)
        
        except Exception as e:
            self.error_tp.typewriter(f"[!!!] Error Loading Data In src/transactions.py: {e}")

        return data
    
    def _save_data(self, data) -> None:
        try:
            with open(self.data_fp, "w") as f:
                json.dump(data, f, indent=2)
        
        except Exception as e:
            self.error_tp.typewriter(f"[!!!] Error Saving Data In src/transactions.py: {e}")
    #endregion

    # Helper Methods
    def _get_time(self) -> str:
        return str(date.today())

    # Transaction Config Methods
    #region
    def transaction_help(self) -> None:
        """
        Transaction Requirements

        ----- Required Input -----
        name
        amount

        ----- Not Required -----
        date if input else use datetime.now()

        """
        
        self.quick_tp.typewriter(
            '----- Required Inputs ----\n-name "Example"  -amount "123.45"\n----- Not Required -----\n-date "1/1/25"'
        )
        print()
        self.quick_tp.typewriter(
            'Example:\n    -name Shopping -amount 150\n    -name "Book Store" -amount "50" -date "12/10/24"'
        )
        self.quick_tp.typewriter("If your transaction name has a space in it, you must use quotation marks.")
        print()
        self.main_tp.inputTypewriter("Press Enter to continue.", end =' ')

    def parse_transaction(self, user_input: list[str]) -> bool:
        # Iterate through each transaction command and see if it starts with -
        user_input = iter(user_input)
        data = {}

        for item in user_input:
            if item.startswith("-"):
                next_item = next(user_input)
                if next_item.startswith('-'):
                    return False
                
                data[item.strip("-")] = next_item.strip('"')
        
        data_keys = data.keys()
        if "name" in data_keys and "amount" in data_keys:
            pass
        else:
            return False

        transaction = {
            "Name": data["name"],
            "Amount": data["amount"],
            "Date": data["date"] if "date" in data.keys() else self._get_time()
        }
        print(transaction)
        input()
        self.data.append(transaction)
        self._save_data(self.data)

        return True

    def display_page(self, index: int) -> None:
        def item_details(item) -> str:
            return f"Name: {item["Name"]}\n    - Amount Paid: {item["Amount"]}\n    - Date of Entry: {item["Date"]}"

        items_to_display = self.data[index:index+self.page_length]

        for i, item in enumerate(items_to_display, index + 1):
            self.quick_tp.typewriter(f"{i}. {item_details(item)}")
            print()
    #endregion

    # Transaction Methods
    #region
    def add_transaction(self) -> None:
        """Add New Transactions"""
        run = True
        while run:
            user_input = self.main_tp.inputTypewriter("Enter in transaction details, Enter E to exit, or type !help for help")

            # Check if user needs help
            if user_input[0].lower().startswith("!h"):
                self.transaction_help()
            
            # Check if user wants to exit
            elif user_input[0].lower().startswith("e"):
                run = False

            else:
                # Start Decoding Input
                fixed_input = user_input.split()
                valid = self.parse_transaction(fixed_input)

                if valid:
                    self.main_tp.typewriter("Added Transaction...")
                else:
                    self.main_tp.typewriter("Transaction not added. Invalid formatting, type !help for help...")

                self.main_tp.inputTypewriter("Press Enter to continue.", end = ' ')

            cc()

    def remove_transaction(self) -> None:
        """Remove Old Transactions"""
        if len(self.data) == 0:
            self.main_tp.typewriter("You have no transactions logged!")
            self.main_tp.inputTypewriter("Press Enter to return to the menu.", end=' ')
            return
    
        current_index = 0

        run = True
        while run:
            if len(self.data) == 0:
                self.main_tp.typewriter("You have no transactions logged!")
                self.main_tp.inputTypewriter("Press Enter to return to the menu.", end=' ')
                run = False
                continue
            
            self.display_page(current_index)

            print()
            self.quick_tp.typewriter("----- Options -----")
            options = [
                "Next" if current_index + self.page_length <= len(self.data) else None,
                "Prev" if current_index > 10 else None,
                "Enter in a transaction number to remove",
                "Exit"
            ]
            for opt in options:
                if opt is not None:
                    self.quick_tp.typewriter(opt)

            user_input = self.main_tp.inputTypewriter("Select an option").upper()

            if user_input.startswith("N") and "Next" in options:
                current_index += self.page_length

            elif user_input.startswith("P") and "Prev" in options:
                current_index -= self.page_length

            elif user_input.startswith("E"):
                run = False
            
            elif user_input.isdigit():
                user_input = int(user_input) - 1
                while True:
                    ui = self.main_tp.inputTypewriter(f"Are you sure you want to remove {self.data[user_input]["Name"]} (Y/N)?")
                    if ui.title().startswith("Y"):
                        self.data.pop(user_input)
                        self._save_data(self.data)
                        break

                    elif ui.title().startswith("N"):
                        break

                    else:
                        self.main_tp.typewriter("That is not an option, type Y or N")
                        print()

            else:
                self.main_tp.typewriter("That is not an option...")
                self.main_tp.inputTypewriter("Press Enter to continue.", end=' ')
            
            cc()

    def view_transactions(self) -> None:
        """
        View All the transactions (10 per page)
        Edit Transactions based on numbered selection (e.g. select which one to edit by index)
        """
        if len(self.data) == 0:
            self.main_tp.typewriter("You have no transactions logged!")
            self.main_tp.inputTypewriter("Press Enter to return to the menu.", end=' ')
            return

        current_index = 0
        
        run = True
        while run:
            self.display_page(current_index)

            print()
            self.quick_tp.typewriter("----- Options -----")
            options = [
                "Next" if current_index + self.page_length <= len(self.data) else None,
                "Prev" if current_index > 10 else None,
                "Exit"
            ]
            for opt in options:
                if opt is not None:
                    self.quick_tp.typewriter(opt)
            
            user_input = self.main_tp.inputTypewriter("Select an option").upper()
            
            if user_input.startswith("N") and "Next" in options:
                current_index += self.page_length

            elif user_input.startswith("P") and "Prev" in options:
                current_index -= self.page_length

            elif user_input.startswith("E"):
                run = False
            
            else:
                self.main_tp.typewriter("That is not an option...")
                self.main_tp.inputTypewriter("Press Enter to continue.", end=' ')
            
            cc()
    #endregion