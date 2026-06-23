from input import parse_input
from classes import AddressBook, Record, input_error
from data import save_data, load_data


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
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
def show_all(book: AddressBook):
    return str(book)


@input_error
def change(args, book):
    book[args[0]].edit_phone(args[1], args[2])
    return "Phone changed"


@input_error
def phone(args, book):
    record = book.find(args[0])
    if record is None:
        return "Contact not found"
    return '; '.join(p.value for p in record.get_phones())


@input_error
def add_birthday(args, book):
    book[args[0]].add_birthday(args[1])
    return "Birthday added"


@input_error
def show_birthday(args, book):
    return book[args[0]].show_birthday()


@input_error
def birthdays(book):
    return "\n".join(birthday for birthday in book.get_upcoming_birthdays())


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change(args, book))
        elif command == "phone":
            print(phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

    save_data(book)
if __name__ == "__main__":
    main()
