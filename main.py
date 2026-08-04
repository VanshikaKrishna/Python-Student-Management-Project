import json
from abc import ABC,abstractmethod
from pathlib import Path

database = "school_data.json"
data = {"students": [], "teachers": []}

if Path(database).exists():
    with open(database, 'r') as f:
        content = f.read()
        if content:
            data = json.loads(content)

def save():
    with open(database, "w") as f:
        json.dump(data, f,indent=4)
class Persons(ABC):

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def validate_email(email):
        if "@" in email  and "." in email:
            return True
        else: 
            return False



class Student(Persons):

    def get_roles(slef):
        return "Student"

    def register(self):
        name = input("tell your name:-")
        age = int(input("tell your age:-"))
        email = input("tell your email:-")
        roll_no = input("tell your roll number:-")

        if not Persons.validate_email(email):
           print("Invalid Email")
           return

        for i in data['students']:
            if i['roll_no'] == roll_no:
                print("Student already exist")
                return

        data['students'].append({
            "name":name,
            "age":age,
            "email":email,
            "roll_no":roll_no,
            "grades":{}
        })
        save()
        print(f"Student {name} registered")

    def show_details(self):
        roll_no = input("Roll no:-")
        for s in data['students']:
            if s['roll_no'] == roll_no:
                grades = s['grades']
            
            # 1. Corrected .values() and calculated length based on values
            avg = sum(grades.values()) / len(grades) if grades else 0

            print(f"\n Name   : {s['name']}")
            print(f" Roll No : {s['roll_no']}")
            print(f" Grades : {s['grades']}")
            
            # 2. Corrected variable placement and float formatting
            print(f" Average : {avg:.2f}") 
            return

    
    def add_grade(self):
        roll_no = input("tell the roll number:-")
        subject = input("Subject :")
        marks = float(input("Marks:-"))

        for i in data['students']:
            if i["roll_no"] == roll_no:
                # Ensure the 'grades' dictionary itself exists first
                if 'grades' not in i:
                    i['grades'] = {}
                
                # FIX: Change '==' to '=' to assign the marks
                i['grades'][subject] = marks
                
                save()
                print("Grade added successfully")
                return
                
        print("Student not found")    

class Teacher(Persons):
    def get_roles(slef):
            return "Teacher"

    def register(self):
            name = input("tell your name:-")
            age = int(input("tell your age:-"))
            email = input("tell your email:-")
            subject = input("Subject:-")
            emp_id = input("tell your emp_id number:-")

            if not Persons.validate_email(email):
               print("Invalid Email")
               return
            
            for i in data['teachers']:
                if i['emp_id'] == emp_id:
                    print("Teacher already exist")
                    return

            data['teachers'].append({
                "name":name,
                "age":age,
                "email":email,
                "subject":subject,
                "emp_id":emp_id,
            })
            save()
            print(f"Teacher {name} registered")

    def show_details(self):
        emp_id = input("Employee ID:")

        for t in data["teachers"]:
            if t["emp_id"] == emp_id:
               print(f" Name : {t['name']}")             
               print(f" Subject : {t['subject']}")             
               print(f" Emp ID : {t['emp_id']}") 
               return
        print("Teacher not found.")          

stud = Student()  
tech = Teacher()   

print("press 1 to register a student")
print("press 2 to register a teacher")
print("press 3 to add grades")
print("press 4 to show a student details")
print("press 5 to show a teacher details")

choice = int(input("Please tell your choice :- "))

if(choice == 1):
    stud.register()

if(choice == 2):
    tech.register()

if(choice == 3):
    stud.add_grade()

if(choice == 4):
    stud.show_details()

if(choice == 5):
    tech.show_details()