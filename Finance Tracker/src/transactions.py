import json
from VividText import VividText as vt

class Transactions:
    def __init__(self, data_fp: str):
        # Base Variables
        self.main_tp = vt(bold=True, sleep=.03)
        self.quick_tp = vt(bold=True, sleep=0)

        # Grab and load the data
        self.data_fp = data_fp
        self.data = self._load_data()

    # Data Handling Methods
    #region
    def _load_data(self) -> list | dict:
        try:
            with open(self.data_fp, "r") as f:
                data = json.load(f)
        
        except Exception as e:
            raise json.JSONDecodeError(f"[!!!] Error Loading Data In src/transactions.py: {e}")

        return data
    
    def _save_data(self, data) -> None:
        try:
            with open(self.data_fp, "w") as f:
                json.dump(data, f)
        
        except Exception as e:
            print(f"[!!!] Error Saving Data In src/transactions.py: {e}")
    #endregion

    # Help Methods
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
            'Example:\n -name "Shopping" -amount "150"\n-name "Book Store" -amount "50" -date "12/10/24"'
        )
        print()
        self.main_tp.inputTypewriter("Press Enter to continue.", end =' ')

    # Transaction Methods
    def add_transaction(self) -> None:
        """Add New Transactions"""
        run = True
        while run:
            user_input = self.main_tp.inputTypewriter("Enter in transaction details, or type !help for help > ")

            # Check if user needs help
            if user_input.lower().startswith("!h"):
                self.transaction_help()
            
            else:
                # Start Decoding Input
                fixed_input = user_input.split()

    def remove_transaction(self) -> None:
        """Remove Old Transactions"""
        pass

    def view_transactions(self) -> None:
        """
        View All the transactions (10 per page)
        Edit Transactions based on numbered selection (e.g. select which one to edit by index)
        """
        pass
