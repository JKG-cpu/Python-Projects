from ..settings import *

class BookManager:
    def __init__(self, file_path):
        self.task_loader = DataLoader(
            file_path = file_path
        )
        self.data = self.task_loader.data

        self.books_per_page = 10

    def create_new_entry(self, name: str, pages: str | int = None, goal: str = None):
        new_book = {
            "Book Name": name,
            "Page Amount": pages,
            "Finish Date": goal
        }
        self.data.append(new_book)
        self.task_loader.save_data(data = self.data)

    def remove_book(self, index):
        self.data.pop(index)
        self.task_loader.save_data(data = self.data)

    def view_books(self):
        """View all books and remove (by number list)"""
        book_index = 0
        run = True
        while run:
            # Load Data
            self.data = self.task_loader._load_data()

            # Exit if no data
            if not self.data:
                break

            # Print Books -> 10 per page
            max_index = min(len(self.data), book_index + 10)
            books = self.data[book_index:max_index]

            for i, book in enumerate(books, start = book_index + 1):
                pPrinter.typewriter(f"{i}. {book['Book Name']}")

            # Ask user for input and print options
            print()
            options = [
                "Type in a number to view a book",
                "Type in E to exit",
                "Type in P for the next page" if len(self.data) > book_index + 10 else "",
                "Type in B for the previous page" if book_index >= 10 else ""
            ]

            mPrinter.typewriter("----- Options -----")
            for i, opt in enumerate(options, start = 1):
                if opt != "":
                    mPrinter.typewriter(f"{i}. {opt}")
                else:
                    pass

            raw_input = mPrinter.inputTypewriter("Enter an option")

            # Book_index += 10 for next page

            run = False