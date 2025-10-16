from os.path import join

from src import *

class Main:
    def __init__(self):
        # File Paths
        self.settings_fp = join("data", "settings.json")
        self.data_fp = join("data", "transactions.json")

        # Classes
        self.settingsConfig = SettingsConfig(self.settings_fp)
        self.transactions = Transactions(self.data_fp)

        # Attributes
    
    