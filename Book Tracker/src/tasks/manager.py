from ..settings import *

class Manager:
    def __init__(self, file_path):
        self.task_loader = DataLoader(
            file_path = file_path
        )
        self.data = self.task_loader.data
