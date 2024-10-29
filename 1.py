from typing import Dict, Set
from pydantic import BaseModel, EmailStr



class Book(BaseModel):
    title: str
    author: str
    year: int
    categories: list[str]
    available: bool
    
    
    def __hash__(self):
        return hash(self.title)


class User(BaseModel):
    name: str
    email: EmailStr
    membership_id : str


    def __hash__(self):
        return hash(self.name)    


class Libarary(BaseModel):
    #словарь с книгами и их количеством 
    books: Dict[Book, int] = dict()
    #слоарь с юзером и сетом взятых им книг 
    users: Dict[User, Set[Book]] = dict()
    
    def add_book(self, book : Book, count : int):

        """
            добавляет книги в словарь  
        """

        if(self.books.get(book) == None):
            self.books[book] = count;
        else:
            self.books[book] = self.books[book] + count

    
    def find_book(self, title: str) -> Book | None:
        """
            ищет книгу в словаре по заголовку
        """

        for book in self.books.keys():
            if(title == book.title):
                return book
            else:
                return None

          
    def is_book_borrow (self, book: Book) -> bool:
        """
            проверяет есть ли книга в наличии  
        """

        if(self.books.get(book) > 0 ):
            return True
        else:
            raise BookNotAvailable('Not found or out of stock')
    

    
    def return_book(self, book: Book, user: User)-> None:
        """
            производит возврат книг
            вовращает книгу в словарь книг
            удаляет книгу из сета взятых книг пользователя 
        """

        self.books[book] = self.books[book] + 1
        self.users[user].remove(book)
        

    def take_book(self, book: Book, user: User) -> None:
        """
            производит взяте книги
            количетво книг в словаре уменьшается
            добавляет книгу в сет взятых книг пользователя 
        """

        self.books[book] = self.books[book] - 1

        if(self.users.get(user) == None):
            self.users[user] = set()
            self.users[user].add(book)
    
        else:
            self.users[user].add(book)
            


    def total_books(self) -> Dict[Book, int]:
        
        for book in self.books.keys():
            print("Книга :", book.title, " ", book.author, ". В наличии: " ,self.books[book] )        

    
class BookNotAvailable(Exception):
    pass

book1 = Book(title = "title1", author = "author", year = 1111 , categories= list(), available = True)
book2 = Book(title = "title2", author = "author", year = 1111 , categories= list(), available = True)
user = User(name="name", email="name@gmail.com", membership_id="asdsad")
lib = Libarary()
lib.add_book(book=book1,count= 2)
lib.add_book(book=book2, count= 1)
lib.take_book(book=book1, user= user)

try:
    print(lib.is_book_borrow(book=book1))
except BookNotAvailable as error:
    print(error)

lib.total_books()
print()
lib.return_book(book=book1,user= user)

lib.total_books()
