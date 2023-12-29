import re
import os

def print_menu() -> None:
    print("1. Create contact")
    print("2. Change contact")
    print("3. Find contact")
    print("4. Delete contact")
    print("5. Show contacts")
    print("6. Copy a contact from another file")
    print("7. Exit")
    print("If you accidentally pressed the wrong button, write 'cancel'")


def contact_exists(contact_book: dict, name: str) -> bool:
    return bool(contact_book.get(name, 0)) 


def valid_number(contact_book: dict, number: str) -> bool:
    # we check if the number is valid using regular expressions
    return re.fullmatch(r'^(8{1}|\+7{1})(\(\d{3}\)\d{3}\-\d{2}\-\d{2}|\d{10})', number) is None


def create_contact(contact_book: dict) -> None:
    name = input("\nName: ")
    if name == "cancel":
        return 
    
    t_number = input("Telephone number: ")
    # the number should be a valid Russian number
    while valid_number(contact_book, t_number):
        # in case user inputs invalid number, we prompt to try again
        t_number = input("You should enter a valid Russian telephone number. Try again: ")
        if t_number == "cancel":
            return 
    
    if not contact_exists(contact_book, name):
        contact_book[name] = t_number
    else:
        print("Name already exists")
        create_contact(contact_book)
    print()


def change_contact(contact_book: dict) -> None:
    option = input("\nDo you want change name or number? ")

    def get_name() -> str:
        name = input("Enter the name of the contact to change: ")
        while not contact_exists(contact_book, name):
            name = input("There's no such contact. Write the name again: ")
            if name == "cancel":
                return ''
        return name
            
    match option:
        case "name":

            name_old = get_name()
            if not name_old:
                return 
            
            name_new = input("A new name for this contact: ")
            while contact_exists(contact_book, name_new):
                name_new = input("A contact with this name already exists. Enter a different name: ")
            
            
            contact_book[name_new] = contact_book[name_old]
            delete_contact(contact_book, name_old)
            print()
  
        case "number":
            name = get_name()
            if not name:
                return 

            new_number = input("Enter a new number: ")

            # the number should be a valid Russian number
            while (valid_number(contact_book, new_number)):
               # in case user inputs invalid number, we prompt to try again
                new_number = input("Invalid number. Try again: ")
                
                if new_number == "cancel":
                    return 
                
            contact_book[name] = new_number
            print()
            
        case "cancel":
            return

        case _:
            print("Enter either 'name' or 'number'")
            change_contact()


def find_contact(contact_book: dict) -> None:
    name = input("\nEnter a name: ")
    print(contact_book.get(name, "No such contact. Use '5. Show contacts'"), '\n')


def delete_contact(contact_book: dict, name: str = None) -> None:
    if name is None:
        show_contacts(contact_book)
        name = input("What contact you'd like to delete: ")
        if not contact_book.get(name, 0):
            return delete_contact(contact_book)
    del contact_book[name]
    print()


def show_contacts(contact_book: dict) -> None:
    print()
    contact_book = dict(sorted(contact_book.items()))
    for name, number in contact_book.items():
        print(f"{name}: {number}")
    print()


def choose_directory() -> str:
    return input("Enter an absolute path to the directory with telephone book text files:\n")


def choose_text_file(dir_path: str) -> str:
    files = [file for file in os.listdir(dir_path.strip("\"")) if file.endswith(".txt")]

    print("\nThose are the text files in this directory:", *[str(i) + ". " + f for i, f in enumerate(files, 1)], sep="\n")

    try:
        file_num = int(input("\nWhich one do you want to open now? (enter a number)\n"))
    except ValueError:
        # in case user enters "cancel"
        return


    while file_num - 1 not in range(len(files)):
        try:
            file_num = int(input("Please, choose a number from the list above.\nNumber: "))
        except ValueError:
            # in case user enters "cancel"
            return
        

    print(f"You're now working with {files[file_num - 1]}\n")
    return files[file_num - 1]


def copy_from_another_file(dir_path: str, contact_book_original: dict, original_file_name: str) -> None:
    file_name = original_file_name
    while condition := (file_name == original_file_name):
        file_name = choose_text_file(dir_path)
        if file_name == "cancel":
            return
        if condition:
            print("You can't copy from the original file!")

    
    with open(file_name, "r") as file:
        contact_book = fill_dict(file)

    print(f"Contacts from {file_name}:")
    show_contacts(contact_book)

    contact_name = input("Which one do you want to copy to another file? (enter a name)\n")
    if not contact_exists(contact_book_original, contact_name):
        while not contact_book.get(contact_name, 0):
            contact_name = input("There's no such contacts in the file. The name: ")
        contact_book_original[contact_name] = contact_book.get(contact_name)
    else:
        print("There's already a contact with this name in the original telephone book")


def fill_dict(file) -> dict:
    contact_book = dict()
    for line in file.readlines():
            name, number = line.split(":")
            contact_book[name] = number[:-1]
    return contact_book
    

def main() -> None:
    dir_path = choose_directory()
    original_file_name = choose_text_file(dir_path)

    with open(original_file_name, "r") as file:
        contact_book = fill_dict(file)
            
    while 1:
        print_menu()
        input_number = input("Choose the number: ")
        match input_number:
            case "1":
                create_contact(contact_book)
                
            case "2":
                change_contact(contact_book)
                
            case "3":
                find_contact(contact_book)

            case "4":
                delete_contact(contact_book)

            case "5":
                show_contacts(contact_book)
            
            case "6":
                copy_from_another_file(dir_path, contact_book, original_file_name)

            case "7":
                print("Thank you for working with us!")
                break
            
            case _:
                print("\nEnter the number provided above!\n")

    with open(original_file_name, "w") as file:
        contact_book = dict(sorted(contact_book.items()))
        for key, value in contact_book.items():
            file.write(f"{key}:{value}\n")
        
if __name__ == "__main__":
    main()
