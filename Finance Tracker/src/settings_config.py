import json
from VividText import VividText as vt

from .helper_functions import *

class SettingsConfig:
    def __init__(self, data_fp: str):
        # Typewriters
        self.main_tp = vt(bold=True, sleep=.03)
        self.quick_tp = vt(bold=True, sleep=0)
        self.error_tp = vt(color="bright_red", bold=True, sleep=0)
    
        # Attributes

        # Data loading
        self.data_fp = data_fp
        self.data = self._load_data()
    
    # Data Methods
    #region
    def _load_data(self) -> dict:
        data = {}
        try:
            with open(self.data_fp, "r") as f:
                data = json.load(f)
        
        except Exception as e:
            self.error_tp.typewriter(f"[!!!] Error loading data: {e}")

        return data

    def _save_data(self) -> None:
        try:
            with open(self.data_fp, "w") as f:
                json.dump(self.data, f, indent = 2)
        
        except Exception as e:
            self.error_tp.typewriter(f"[!!!] Error Saving data: {e}")
    #endregion

    # Setting Config Methods
    def switch_currency(self) -> None:
        currency_options = self.data["Currency Options"]
        run = True

        while run:
            # Display currency options
            self.main_tp.typewriter("----- Currency Options -----")
            self.main_tp.menuTypewriter(" | ", currency_options)

            # Ask user for the currency they would like to switch too
            user_input = self.main_tp.inputTypewriter("Select a current you would like to switch to or type E to exit")

            # Find currency option
            if user_input.upper() in currency_options:
                self.data["Currency"] = user_input.upper()
                self._save_data()
                self.main_tp.typewriter("Settings Saved!")
                self.main_tp.inputTypewriter("Press Enter to continue.", end = " ")

            elif user_input.upper().startswith("E"):
                run = False
                
            else:
                self.main_tp.typewriter("That is not a valid option...")
                self.main_tp.inputTypewriter("Press Enter to continue.", end=' ')

            cc()

    def setup_categories(self) -> None:
        pass
            