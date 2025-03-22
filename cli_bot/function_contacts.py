from functools import wraps
from addres_book import AddressBook, Record
from get_upcoming_birthdays import get_upcoming_birthdays


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return f"Contact not found."
        except IndexError:
            return "Please enter 'Name'"
        except Exception as e:
            return f"Unexpected error: {e}"
          
    return inner


def parse_input(user_input):
    params = user_input.split()
    if not params:
        return "", []
    cmd, *args = params
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Please provide name and phone number"
    name, phone, *_ = args 
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        record.add_phone(phone)
        return "Contact added."
    if any(phone_number.value == phone for phone_number in record.phones):
        return f"Phone number already exists: {phone}."
    record.add_phone(phone)
    return "Phone number added to existing contact."


@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        return "Please provide name, old phone number and new phone number"
    name, old_phone, new_phone, *_ = args 
    record = book.find(name)
    if record is None:
        return "Contact not found"
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        return "Please provide name"
    name, *_ = args 
    record = book.find(name)
    if record is None:
        return "Contact not found"
    phones = ', '.join(phone.value for phone in record.phones)
    return phones


def show_all(book: AddressBook):
    if not book.data:
        return "No contacts available."
    
    contacts = [f"Name: {record.name.value}, Phones: {', '.join(p.value for p in record.phones)}"
                for record in book.data.values()]
    
    return "\n".join(contacts)


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        return "Please provide both name and birthday in the format: 'Name DD.MM.YYYY'"
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found"
    elif record.birthday:
        return f"Birthday already exists for {name}"
    record.add_birthday(birthday)
    return f"Birthday added for {name}"


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        return "Please provide name"
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found"
    if record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    return f"{name} has no birthday saved."


@input_error
def birthdays(book: AddressBook):
    records = list(book.values())
    upcoming = get_upcoming_birthdays(records)
    if not upcoming:
        return "No upcoming birthdays found in the next 7 days."
    return f"Список привітань на цьому тижні:\n{"\n".join([f"{entry['name']}: {entry['birthday']}" for entry in upcoming])}"

