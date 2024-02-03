import pickle
from collections import UserDict
from datetime import date, datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
    
    def valid_phone(self):
        if self.value is not None:
            if len(self.value) != 10 or not self.value.isdigit():
                raise ValueError("Invalid phone number")
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        self.valid_phone() 

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
    
    def valid_birthday(self):
        if self.value is not None:
            if not isinstance(self.value, str):
               raise ValueError('Invalid birthday date')
        else:
            pass
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        self.valid_birthday() 
     
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number:str):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number:str):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return

    def find_phone(self, phone_number:str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
    
    def edit_phone(self, old_phone:str, new_phone:str):
        for phone in self.phones:
            if phone.valid_phone and phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError('Invalid phone number')

    def add_birthday(self, birthday:str):
        self.birthday = Birthday(birthday)
        return
    
    def days_to_birthday(self, name:str):
        current_year = date.today().year           
        if self.birthday:
            if self.birthday.valid_birthday:
                convert_str_to_date = datetime.fromisoformat(self.birthday.value).date()
                current_birthday = convert_str_to_date.replace(year=current_year)
                
                days_to_birthday = abs((date.today() - current_birthday).days)

                return days_to_birthday
        raise ValueError(print("Birthday date is not found"))
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
    
    def __repr__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data[record.name.value]=record

    def find(self, name:str):
        if name in self.data:
            return self.data[name]
        
    def delete(self, name:str):
        if name in self.data:
            del self.data[name]
    
    def iterator(self, N=1):
        return ListIterator(self, N)
        
class ListIterator:
    def __init__(self, AddressBook, N):
        self.index = 0
        self.countable_data = list(AddressBook.data.values())
        self.N = N     

    def __next__(self):
        if self.index < len(self.countable_data):
            records_chunk = self.countable_data[self.index:self.index+self.N]
            self.index += self.N
            #print('===================')
            return records_chunk
        else:
            raise StopIteration()
    
    def __iter__(self):
        return self

book = AddressBook()  

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("1976-12-12")

# Додавання запису John до адресної книги
print(book.add_record(john_record))

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Створення та додавання нового запису для Moa
moa_record = Record("Moa")
moa_record.add_phone("9111000000")
book.add_record(moa_record)
moa_record.add_birthday("1995-01-27")

# Створення та додавання нового запису для Lynn
lynn_record = Record("Lynn")
lynn_record.add_phone("7811000000")
book.add_record(lynn_record)

# Створення та додавання нового запису для Poul
poul_record = Record("Poul")
poul_record.add_phone("5551000000")
book.add_record(poul_record)

# Вивід адресної книги
for name, record in book.data.items():
   print(record)


# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
john_days_to_birthday = john.days_to_birthday('John')
print('john_days_to_birthday', john_days_to_birthday)

# Ітерування по адресній книзі
for i in book.iterator(2):
    print(i)

file_name = 'data.bin'

with open(file_name, "wb") as fh:
    pickle.dump(book, fh)


with open(file_name, "rb") as fh:
    unpacked = pickle.load(fh)


print(unpacked)  
print(type(unpacked))

for line in unpacked.iterator(1):
        print(line)

def find_data(str_data: str):
    for line in unpacked.iterator(1):
        line = str(line)
        if str_data in line:
            print(f'possible match is {line}')
    return

print(find_data('1995'))
print(find_data('Ja'))