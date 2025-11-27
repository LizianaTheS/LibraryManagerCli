import typer

app = typer.Typer()


def menu():
    while True:
        print("\nLibrary Management System")
        print("1. Add New Book")
        print("2. Display All Books")
        print("3. Search Book")
        print("4. Remove or Edit Book")
        print("5. Borrow or Return Book")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            display_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            remove_or_edit()
        elif choice == "5":
            borrow_or_return()
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")


def add_book():
    title = input("Title: ")
    genre_id = input("Genre ID: ")
    print(f"Fake-adding book: {title} (Genre {genre_id})")
    input("Press Enter to go back...")


def display_books():
    print("Displaying all books...")
    input("Press Enter to go back...")


def search_book():
    q = input("Search query: ")
    print(f"Searching for {q}...")
    input("Press Enter to go back...")


def remove_or_edit():
    print("Here you can remove/edit...")
    input("Press Enter to go back...")


def borrow_or_return():
    print("Borrow or return menu...")
    input("Press Enter to go back...")


@app.command()
def run():
    menu()


if __name__ == "__main__":
    app()
