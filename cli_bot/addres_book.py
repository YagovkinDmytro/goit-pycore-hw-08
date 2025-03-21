from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value.strip():
            raise ValueError("Name cannot be empty")


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value.isdigit():
            raise ValueError("Phone must contain only digits")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits long")
        
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


    def __repr__(self):
        if self.birthday:
            return f"(name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday})"
        else:
            return f"(name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        
    def remove_phone(self, value):
        self.phones = [phone for phone in self.phones if phone.value != value]

    def edit_phone(self, value, new_value):
        found = any(phone.value == value for phone in self.phones)
        if found:
            self.phones = [Phone(new_value) if phone.value == value else phone for phone in self.phones]
        else:
            raise ValueError("Phone number not found")
    
    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return f"Phone number {value} not found"
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        self.data.pop(name)

    def __str__(self):
        return f"Contacts book: {self.data}"
    
    def __repr__(self):
        return f"AddressBook({self.data})"