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
            'Example:\n    -name "Shopping" -amount "150"\n    -name "Book Store" -amount "50" -date "12/10/24"'
        )
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

    # Transaction Methods
    def add_transaction(self) -> None:
        """Add New Transactions"""
        run = True
        while run:
            user_input = self.main_tp.inputTypewriter("Enter in transaction details, or type !help for help")

            # Check if user needs help
            if user_input.lower().startswith("!h"):
                self.transaction_help()
            
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
        pass

    def view_transactions(self) -> None:
        """
        View All the transactions (10 per page)
        Edit Transactions based on numbered selection (e.g. select which one to edit by index)
        """
        pass