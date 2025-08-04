# Import Packages
import csv
import os
import re
# import pandas as pd

class EmployeeManager:
    
    def __init__(self):
        self.header = ['id', 'name', 'position', 'salary', 'email']
        self.employee = {}
        self.employees = []
        self.index = 0

    def add_to_csv(self, file_status, addOne_or_addAll):
        with open('employees.csv', file_status, newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.header)
            if file_status == 'w':
                writer.writeheader()
            if addOne_or_addAll == self.employee:
                writer.writerow(self.employee)
            else:
                writer.writerows(self.employees)
        
    def add_employee(self, *args):
        self.employee = dict(zip(self.header, args))

        file_exists = os.path.isfile('employees.csv')
        file_status = 'a' if file_exists else 'w'
        self.add_to_csv(file_status, self.employee)
        # print("Saved Successfully")

    def view_all_employees(self):
        self.employees = []
        with open('employees.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.employees.append(dict(row))
        return self.employees

    def update_employee(self, idd, **kwargs):
        self.search_employee(idd)
        for key, value in kwargs.items():
            self.employee[key] = value
        # Replace the old employee data with the updated one
        self.employees[self.index] = self.employee
        # Save the employees back to the file
        self.add_to_csv('w', self.employees)
        # print("Employee updated successfully.")

    def delete_employee(self, idd):
        self.search_employee(idd)
        del self.employees[self.index]
        # Save the employees back to the file
        self.add_to_csv('w', self.employees)
        # print("Employee deleted successfully.")

    def search_employee(self, idd):
        self.view_all_employees()
        matched = [(index, employee) for index, employee in enumerate(self.employees) if employee['id'] == f"{idd}"]
        if not matched: 
            return 0
            # print(f"No employee found with ID {idd}")            
        self.index, self.employee = matched[0]
        return self.employees[self.index]

    def re(self):
        print(self.employees)

emp = EmployeeManager()

# The main menu
def entry():
    inp = 0
    while inp not in range(1, 7):
        inp = int(input("Select your action number:\n 1. Add \n 2. Update \n 3. Delete \n 4. Search \n 5. List all employees \n 6. Exit \n"))
        print("------------------------------\n")
    return inp

def vaildate_id():
    while True:
        idd = input("ID: ")
        try:
            idd = int(idd)
            if idd < 0:
                print("Enter a valid ID...")
                continue
            if emp.search_employee(str(idd)):
                print("ID already exists. Enter a unique ID...")
                continue
            # valid and unique ID
            return idd
        except ValueError:
            print("Enter a valid numeric ID...")

def vaildate_salary(salary=None):
    while True:
        if salary == None:
            salary = input("Salary: ")
        try:
            salary = int(salary)
            if salary < 0:
                print("Salary must be a positive number.")
                salary = None
                continue
            return salary
        except ValueError:
            print("Enter a valid Salary: ")
            salary = None

def vaildate_email(email=None):
    email_pattern = r"^[a-zA-Z]+@gmail+\.(com|net)$"
    while True:
        if email == None:
            email = input("Email: ")
        if re.match(email_pattern, email):
            return email
        else:
            print("Enter a valid email: ")
            email = None

# Main Programme
while True:
    print("------------------------------\n")
    inp = entry()
    match inp:
        case 1: # Add
            print("Enter the employee details")
            # ID
            idd = vaildate_id()   
            # Name
            name = input("Name: ")
            # Position
            position = input("Position: ")
            # Salary
            salary = vaildate_salary()
            # Email
            email = vaildate_email()
            # Add the new employee
            emp.add_employee(idd, name, position, salary, email)
            print("Employee added Successfully")
            
        case 2: # Update
            idd = input("ID: ")
            while emp.search_employee(idd) == 0:
                print(f"No employee found with ID {idd}")
                idd = input("ID: ")
            print("The employee data: ")
            print(emp.search_employee(idd))
            
            update_choice = input("Write the feature you want to update:\n 1. name\n 2. position\n 3. salary\n 4. email\n")
            if update_choice not in ['name', 'position', 'salary', 'email']:
                print("Choose a the correct feature you want to update...")
                continue
            new_value = str(input("The new value: "))
            
            if update_choice == 'salary':
                new_value = vaildate_salary(new_value)
            elif update_choice == 'email':
                new_value = vaildate_email(new_value)
            emp.update_employee(idd, **{update_choice: new_value})
            print("Employee updated successfully.")
        
        case 3: # Delete
            idd = input("ID: ")
            while emp.search_employee(idd) == 0:
                print(f"No employee found with ID {idd}")
                idd = input("ID: ")
            print("The employee data:\n", emp.search_employee(idd))
            check = input("Press y to Confirm or n to back to the main menu.")
            if check == 'y':
                emp.delete_employee(idd)
                print("Employee deleted successfully.")
            else:
                print("Price 'y' or 'n' only...")
                continue
                
        case 4: # Search
            idd = input("ID: ")
            while emp.search_employee(idd) == 0:
                print(f"No employee found with ID {idd}")
                idd = input("ID: ")
            print("The employee data:\n", emp.search_employee(idd))
            
        case 5: # List all employees
            print("All Emplyees:\n")
            for e in emp.view_all_employees():
                print(e)
            # print(pd.DataFrame(pd.read_csv('employees.csv')))
            
        case 6: # Exit
            print("Bye Bye")
            break