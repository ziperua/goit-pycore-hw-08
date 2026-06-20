from input import parse_input
from classes import AddressBook, Record, input_error
from data import save_data, load_data

# @input_error
# def add_contact(args, book):
#     book.add_record(Record(args[0]))
#     if len(args) > 1:
#         i = 1
#         while i < len(args):
#             book[args[0]].add_phone(args[i])
#             i += 1
        

@input_error
def change_phone(args, book):
    return book[args[0]].edit_phone(args[1], args[2])

@input_error
def find_phone_owner(args, book):
    return book[args[0]].find_phone_owner()

@input_error
def add_birthday(args, book):
    return book[args[0]].add_birthday(args[1])

@input_error
def show_birthday(args, book):
    return book[args[0]].show_birthday()

# @input_error
# def get_upcoming_birthdays(book):
#     for contact in book.get_upcoming_birthdays():
#         print(contact)


def main():
    #book = AddressBook()
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
            print(AddressBook.add_contact(args, book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == "phone":
            print(find_phone_owner(args, book))
        elif command == "all":
            for element in book.values():
                print(element)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            for line in book.get_upcoming_birthdays():
                print(line)
        else:
            print("Invalid command.")

    save_data(book)


if __name__ == "__main__":
    main() 