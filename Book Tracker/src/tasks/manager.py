from ..settings import *

class BookManager:
    def __init__(self, file_path):
        self.task_loader = DataLoader(
            file_path = file_path
        )
        self.data = self.task_loader.data

    def create_new_entry(self, name: str, pages: str | int = None, goal: str = None):
        new_book = {
            "Book Name": name,
            "Page Amount": pages,
            "Finish Date": goal
        }
        self.data.append(new_book)
        self.task_loader.save_data(data = self.data)