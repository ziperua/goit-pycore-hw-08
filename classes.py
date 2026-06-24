from collections import UserDict
import datetime as dt


def input_error(function):
    def inner(*args):
        try:
            return function(*args)
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
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone must contain 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = dt.datetime.strptime(value, "%d.%m.%Y").strftime("%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # @input_error
    # def remove_phone(self, phone):
    #     phone_obj = self.find_phone(phone)
    #     if phone_obj: self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone_number(old_phone)
        if phone_obj is None:
            raise ValueError("Phone not found")
        phone_obj.value = Phone(new_phone).value

    def find_phone_number(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def get_phones(self):
        return self.phones

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        return self.birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    # @input_error
    # def delete(self, record):
    #     if record in self.data:
    #         del self.data[record]

    # def get_upcoming_birthdays(self):
    #     week = []
    #     today = dt.date.today()
    #     i = 0
    #     while i < 7:
    #         week.append(dt.date.today() + dt.timedelta(i))
    #         i += 1

    #     for record in self.data.values():
    #         if record.birthday is None:
    #             continue

    #         day, month, _ = record.birthday.value.split(".")
    #         year = dt.date.today().year
    #         if len(month) == 1:
    #             compare = f"{year}-0{month}-{day}"  # 0{month} because datetime getting month like this
    #         else:
    #             compare = f"{year}-{month}-{day}"
    #         str_week = [str(date) for date in week]
    #         date_only = record.birthday.value.split(".")
    #         for date in str_week:
    #             if compare == date:
    #                 yield f"{record.name}: {date_only[0]}.{date_only[1]}"
    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = dt.date.today()

        for record in self.data.values():
            if record.birthday is None:
                continue

            day, month, year = record.birthday.value.split(".")
            birthday_this_year = dt.date(today.year, int(month), int(day))

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= 7:
                if birthday_this_year.weekday() >= 5:
                    days_ahead = 7 - birthday_this_year.weekday()
                    birthday_this_year = birthday_this_year + dt.timedelta(
                        days=days_ahead
                    )

                upcoming_birthdays.append(
                    {
                        "name": str(record.name),
                        "congratulation_date": birthday_this_year.strftime("%d.%m"),
                    }
                )

        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
