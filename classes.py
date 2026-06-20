from collections import UserDict
import datetime as dt

def input_error(function):
    def inner(*args):
        try: return function(*args)
        except ValueError:
            return "Give me valid arguments"
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Enter correct name"
    return inner

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
		pass

class Phone(Field):
    def __init__(self, value):
        if not(value.isdigit() and len(value) == 10):
            raise ValueError("Phone must contain 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            day, month, year = value.split('.')
            day, month, year = int(day), int(month), int(year)
            if day > 31 or day < 1 or month > 12 or month < 1:
                raise ValueError(print("Use real date in format DD.MM.YYYY and"))
            self.value = value
            
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    @input_error
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return "Phone added"
    
    # @input_error
    # def remove_phone(self, phone):
    #     phone_obj = self.find_phone(phone)
    #     if phone_obj: self.phones.remove(phone_obj)

    @input_error
    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone_number(old_phone)
        if phone_obj is None:
            raise ValueError("Phone not found")
        phone_obj.value = Phone(new_phone).value
        return "Phone changed"

    @input_error
    def find_phone_number(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    @input_error
    def find_phone_owner(self):
        return '; '.join(p.value for p in self.phones)

    @input_error
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return "Birthday added"

    @input_error
    def show_birthday(self):
        return self.birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    @input_error
    def add_record(self, record):
        self.data[record.name.value] = record
        return "Contact added"
    
    @input_error
    def add_contact(args, book: AddressBook):
        name, phone, *_ = args
        Phone(phone)
        record = book.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        return message

    
    @input_error
    def find(self, name):
        return self.data.get(name)

    # @input_error
    # def delete(self, record):
    #     if record in self.data:
    #         del self.data[record]

    @input_error
    def get_upcoming_birthdays(self):
        week = []
        today = dt.date.today()
        i = 0
        while i < 7:
            week.append(dt.date.today() + dt.timedelta(i))
            i+=1
        
        for record in self.data.values():
            if record.birthday == None:
                continue

            day, month, _ = record.birthday.value.split('.')
            year = dt.date.today().year
            if len(month) == 1:
                compare = f"{year}-0{month}-{day}" # 0{month} because datetime getting month like this
            else:
                compare = f"{year}-{month}-{day}"
            str_week = [str(date) for date in week]

            for date in str_week:
                if compare == date:
                    yield f"{record.name}: {record.birthday.value}"
        
    # @input_error
    # def all_contacts(self):
    #     for record in self.data.values():
    #         #return record

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())