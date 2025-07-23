from student import Student
from pymongo import MongoClient

class Admin(Student):
    def __init__(self, first, last, username, password):
        super().__init__(first, last, username, password, isAdmin=True)

    