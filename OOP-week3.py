class BookAndMagazine():
    def __init__(self, language, fantasy, horror, fashion, cooking, sports):
        self.language = language
        self.fantasy = fantasy
        self.Horror = horror
        self.fashion = fashion
        self.cooking = cooking
        self.sports = sports

    def numOfBooksAndMagazines(self):
        self.language = 1        
        self.fantasy = 1
        self.horror = 1
        self.fashion = 1
        self.cooking = 1
        self.sports = 1            
             
class Member():
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

class Library():
    def __init__(self):
        self.book_and_magazine = []
        self.members = [] 

    def Register_Member(self, name):
        new_member = Member(name)
        self.members.append(new_member)
        print(f"Member '{name}' registered succesfully")
               
class method():
    def __init__(self, borrowbook, returnbook):
        print("choose borrowbook = 1 or return book =2")


