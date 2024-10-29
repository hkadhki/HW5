from typing import Dict, Set
from pydantic import BaseModel, EmailStr



class Book():

    def __init__(self, title: str, author: str, year: int, categories: list[str]):
        self.title = title
        self.author = author
        self.year = year
        self.available = True
        self.categories = categories
    
    def __hash__(self):
        return hash(self.title)


class User():
    def __init__(self, name, email : EmailStr , membership_id : str ):
        self.name = name
        self.email = email
        self.membership_id = membership_id

    def __hash__(self):
        return hash(self.name)    


class Libarary():
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

book1 = Book("title1", "author", 1111 , list())
book2 = Book("title2", "author", 1111 , list())
user = User("name", "name@gmail.com", "asdsad")
lib = Libarary
lib.add_book(lib, book1, 2)
lib.add_book(lib, book2, 1)
lib.take_book(lib,book1,user)

try:
    print(lib.is_book_borrow(lib,book1))
except BookNotAvailable as error:
    print(error)

lib.total_books(lib)
print()
lib.return_book(lib,book1,user)

lib.total_books(lib)
