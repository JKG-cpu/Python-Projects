from ..settings import *

class BookManager:
    def __init__(self, file_path):
        self.task_loader = DataLoader(
            file_path = file_path
        )
        self.data = self.task_loader.data

        self.books_per_page = 10

    def create_new_entry(self, name: str, pages: str | int = None, goal: str = None, pages_read = None):
        new_book = {
            "Book Name": name,
            "Page Amount": pages.strip('"') if pages else pages,
            "Finish Date": goal.strip('"') if goal else goal,
            "Pages Read": pages_read.strip('"') if pages_read else pages_read
        }
        self.data.append(new_book)
        self.task_loader.save_data(data = self.data)

    def remove_book(self, index):
        self.data.pop(index)
        self.task_loader.save_data(data = self.data)

    def book_details(self, book_data):
        def display_data():
            pPrinter.typewriter(f"Book Name: {book_data["Book Name"]}")
            pPrinter.typewriter(f"    - Pages: {book_data["Page Amount"] if book_data["Page Amount"] else "Not set."}")
            pPrinter.typewriter(f"    - Pages Read: {book_data["Pages Read"] if book_data["Pages Read"] else "Not set."}")
            pPrinter.typewriter(f"    - Finish Data: {book_data["Finish Date"] if book_data["Finish Date"] else "Not set."}")

        options = [
            "Change Page Amount",
            "Change Pages Read",
            "Change Finish Date",
            "Remove Entry",
            "Exit"
        ]
        
        delete = False
        run = True
        while run:
            cc()

            display_data()

            print()
            mPrinter.typewriter("----- Options -----")
            for i, opt in enumerate(options, start = 1):
                pPrinter.typewriter(f"{i}. {opt}")
            print()

            raw_input = mPrinter.inputTypewriter("Select an option")

            if raw_input.isdigit():
                raw_input = int(raw_input)
            
                # Change Page Amount
                if raw_input == 1:
                    new_input = pPrinter.inputTypewriter("Enter a new page amount")
                    book_data["Page Amount"] = new_input

                # Change Pages read
                elif raw_input == 2:
                    new_input = pPrinter.inputTypewriter("Enter pages read")
                    book_data["Pages Read"] = new_input

                # Change Due Date
                elif raw_input == 3:
                    new_input = pPrinter.inputTypewriter("Enter a new due date")
                    book_data["Finish Date"] = new_input

                # Exit
                elif raw_input == 4:
                    delete = True
                    run = False
                
                elif raw_input == 5:
                    run = False

                else:
                    mPrinter.inputTypewriter("That is not a valid option. Press Enter to continue.", end='')

            else:
                mPrinter.inputTypewriter("That is not a valid option. Press Enter to continue.", end='')

        return book_data if not delete else True

    def view_books(self):
        """View all books and remove (by number list)"""
        book_index = 0
        run = True
        while run:
            # Load Data
            self.data = self.task_loader._load_data()

            # Exit if no data
            if not self.data:
                mPrinter.typewriter("No books saved...")
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
                "Type in D to delete all books",
                "Type in P for the next page" if len(self.data) > book_index + 10 else "",
                "Type in B for the previous page" if book_index >= 10 else ""
            ]

            mPrinter.typewriter("----- Options -----")
            for i, opt in enumerate(options, start = 1):
                if opt != "":
                    mPrinter.typewriter(f"{i}. {opt}")
                else:
                    pass

            raw_input = mPrinter.inputTypewriter("Input").title()

            if raw_input.isdigit():
                book_data = self.book_details(self.data[int(raw_input) - 1])
                if book_data == True:
                    self.data.pop(int(raw_input) - 1)
                    self.task_loader.save_data(self.data)
                else:
                    self.data[int(raw_input) - 1] = book_data

            else:
                if raw_input.startswith("E"):
                    run = False

                elif raw_input.startswith("P") and "Type in P for the next page" in options:
                    book_index += 10

                elif raw_input.startswith("B") and "Type in B for the previous page" in options:
                    book_index -= 10
                
                elif raw_input.startswith("D"):
                    self.data = []
                    self.task_loader.save_data(self.data)
                    mPrinter.typewriter("All books removed!")

                else:
                    mPrinter.typewriter("Invalid input...")

            cc()