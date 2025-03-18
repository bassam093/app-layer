class BookAndMagazine:
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre
        self.is_borrowed = 0

                     
class Member():
    def __init__(self, name):
        self.name = name
        self.borrowed_items = []

class Library():
    def __init__(self):
        self.items = []
        self.members = [] 

    def register_member(self, name):
        new_member = Member(name)
        self.members.append(new_member)
        print(f"Member '{name}' registered succesfully")

    def add_item(self, title, genre):
        new_item = BookAndMagazine(title, genre)
        self.items.append(new_item)
        print(f"Item '{title}' added to the library.")
        

    def borrow_item(self, member_name, item_title):
        member = next((m for m in self.members if m.name == member_name), None)
        item = next((i for i in self.items if i.title == item_title), None) 
    
        if member and item:
            item.is_borrowed = 1
            member.borrowed_items.append(item)
            print(f"Item '{item_title}' borrowed by '{member_name}'.")
        else:
            print("Error")

    def return_item(self, member_name, item_title):
        member = next((m for m in self.members if m.name == member_name), None)
        if member:
            item = next((i for i in member.borrowed_items if i.title == item_title), None)
            if item:
                item.is_borrowed = 0
                member.borrowed_items.remove(item)
                print(f"Item '{item_title}' returned by '{member_name}'.")
                return
        print("Error: Either the member or the item was not found.")

    def display_status(self):
        print("\nLibrary Status:")
        
        print("Books and Magazines:")
        for item in self.items:
            status = "Borrowed" if item.is_borrowed else "Available"
            print(f"- {item.title} ({item.genre}): {status}")

        print("\nMembers:")
        for member in self.members:
            borrowed_titles = [item.title for item in member.borrowed_items]
            print(f"- {member.name}: Borrowed Items: {borrowed_titles}")


def main():
    library = Library()

    while True:
        print("\nLibrary Management System")
        print("1. Register Member")
        print("2. Add Book/Magazine")
        print("3. Borrow Item")
        print("4. Return Item")
        print("5. Display Status")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter member name: ")
            library.register_member(name)
        elif choice == "2":
            title = input("Enter item title: ")
            genre = input("Enter item genre: ")
            library.add_item(title, genre)
        elif choice == "3":
            member_name = input("Enter member name: ")
            item_title = input("Enter item title: ")
            library.borrow_item(member_name, item_title)
        elif choice == "4":
            member_name = input("Enter member name: ")
            item_title = input("Enter item title: ")
            library.return_item(member_name, item_title)
        elif choice == "5":
            library.display_status()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()