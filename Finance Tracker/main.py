from os.path import join

from src import *

data_fp = join("data", "transactions.json")

Transactions(data_fp).add_transaction()