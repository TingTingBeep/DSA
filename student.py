class Student:
    def __init__(self, student_id, name, course, year_level):
        self.student_id = student_id
        self.name = name
        self.course = course
        self.year_level = year_level

    def __str__(self):
        return (f"Student ID : {self.student_id}\n"
                f"Name       : {self.name}\n"
                f"Course     : {self.course}\n"
                f"Year Level : {self.year_level}")

    def to_row(self):
        return f"{self.student_id:<12}{self.name:<25}{self.course:<10}{self.year_level:<5}"


class DynamicArray:
    INITIAL_CAPACITY = 5

    def __init__(self):
        self._capacity = DynamicArray.INITIAL_CAPACITY
        self._data = self._allocate(self._capacity)
        self._size = 0

    @staticmethod
    def _allocate(capacity):
        raw = []
        i = 0
        while i < capacity:
            raw += [None]
            i += 1
        return raw

    def _resize(self, new_capacity):
        new_data = self._allocate(new_capacity)
        i = 0
        while i < self._size:
            new_data[i] = self._data[i]
            i += 1
        self._data = new_data
        self._capacity = new_capacity

    def size(self):
        return self._size

    def capacity(self):
        return self._capacity

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def add(self, student):
        if self.is_full():
            self._resize(self._capacity * 2)
        self._data[self._size] = student
        self._size += 1

    def get(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds.")
        return self._data[index]

    def set(self, index, student):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds.")
        self._data[index] = student

    def index_of(self, student_id):
        i = 0
        while i < self._size:
            if self._data[i].student_id == student_id:
                return i
            i += 1
        return -1

    def remove_at(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds.")
        i = index
        while i < self._size - 1:
            self._data[i] = self._data[i + 1]
            i += 1
        self._data[self._size - 1] = None
        self._size -= 1

    def display(self):
        if self.is_empty():
            print("No student records found.")
            return
        print(f"{'ID':<12}{'Name':<25}{'Course':<10}{'Year':<5}")
        print("-" * 52)
        i = 0
        while i < self._size:
            print(self._data[i].to_row())
            i += 1


class StudentRecordManager:
    RANDOM_FIRST_NAMES = ["Juan", "Maria", "Pedro", "Ana", "Carlo", "Liza",
                           "Mark", "Grace", "Jose", "Ella"]
    RANDOM_LAST_NAMES = ["Dela Cruz", "Santos", "Reyes", "Garcia", "Torres",
                          "Bautista", "Ramos", "Flores", "Mendoza", "Aquino"]

    def __init__(self):
        self.records = DynamicArray()

    @staticmethod
    def _generate_random_name():
        import random
        first = random.choice(StudentRecordManager.RANDOM_FIRST_NAMES)
        last = random.choice(StudentRecordManager.RANDOM_LAST_NAMES)
        return f"{first} {last}"

    def add_student(self):
        print("\n--- Add Student ---")
        student_id = input("Enter Student ID: ").strip()

        if self.records.index_of(student_id) != -1:
            print("A student with that ID already exists.")
            return

        name = input("Enter Student Name (leave blank for a random name): ").strip()
        if name == "":
            use_random = input("No name entered. Generate a random name? (y/n): ").strip().lower()
            if use_random == "y":
                name = self._generate_random_name()
                print(f"Generated name: {name}")
            else:
                while name == "":
                    name = input("Enter Student Name: ").strip()

        course = input("Enter Course: ").strip()
        year_level = self._read_int("Enter Year Level: ")

        was_full = self.records.is_full()
        self.records.add(Student(student_id, name, course, year_level))

        if was_full:
            print(f"Array was full. Capacity increased to {self.records.capacity()}.")
        print("Student added successfully.")

    def display_students(self):
        print("\n--- Student List ---")
        self.records.display()

    def search_student(self):
        print("\n--- Search Student ---")
        student_id = input("Enter Student ID to search: ").strip()
        index = self.records.index_of(student_id)
        if index == -1:
            print("Student not found.")
        else:
            print("Student found:")
            print(self.records.get(index))

    def update_student(self):
        print("\n--- Update Student ---")
        student_id = input("Enter Student ID to update: ").strip()
        index = self.records.index_of(student_id)
        if index == -1:
            print("Student not found.")
            return

        student = self.records.get(index)
        print("Leave a field blank to keep its current value.")

        new_name = input(f"Name [{student.name}]: ").strip()
        new_course = input(f"Course [{student.course}]: ").strip()
        new_year = input(f"Year Level [{student.year_level}]: ").strip()

        if new_name:
            student.name = new_name
        if new_course:
            student.course = new_course
        if new_year:
            if new_year.isdigit():
                student.year_level = int(new_year)
            else:
                print("Invalid year level input ignored.")

        self.records.set(index, student)
        print("Student updated successfully.")

    def remove_student(self):
        print("\n--- Remove Student ---")
        student_id = input("Enter Student ID to remove: ").strip()
        index = self.records.index_of(student_id)
        if index == -1:
            print("Student not found.")
            return
        self.records.remove_at(index)
        print("Student removed successfully.")

    def display_array_info(self):
        print("\n--- Array Information ---")
        print(f"Number of students : {self.records.size()}")
        print(f"Current capacity   : {self.records.capacity()}")

    @staticmethod
    def _read_int(prompt):
        while True:
            value = input(prompt).strip()
            if value.isdigit():
                return int(value)
            print("Invalid input. Please enter a whole number.")


def print_menu():
    print("\n===== STUDENT RECORD MANAGER =====")
    print("1. Add Student")
    print("2. Display Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Remove Student")
    print("6. Display Array Information")
    print("7. Exit")


def main():
    manager = StudentRecordManager()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            manager.add_student()
        elif choice == "2":
            manager.display_students()
        elif choice == "3":
            manager.search_student()
        elif choice == "4":
            manager.update_student()
        elif choice == "5":
            manager.remove_student()
        elif choice == "6":
            manager.display_array_info()
        elif choice == "7":
            print("Exiting Student Record Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()