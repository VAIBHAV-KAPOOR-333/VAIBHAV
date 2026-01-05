# print('hello')
# for i in range(5):
#     if i == 3:
#         continue  
#     print(i)
# for i in range(5):
#     if i == 3:
#         break
#     print(i)
# for i in range(5):
#     if i == 3:
#         pass 
#     print(i)
'''t=0
arr=[1,2,3]
for i in arr:
    print(i)
    t+=i
print(t)'''
# n=int(input())
# def check_even_odd(a):
#     if a%2==0:
#         return "even"
#     else:
#         return "odd"
# print(check_even_odd(n))  
# student = {
#     "name": "Alex",
#     "age": 20,
#     "grade": "A"
# }
# for item in student.items():
#     print(item)
# for item in student.items():
#     key = item[0]
#     value = item[1]
#     print(key, ":", value)
# for key, value in student.items():
#      print(key,":",value)
     
# Step 1: Get student name
'''name = input("Enter student name: ")

# Step 2: Subjects list
subjects = ["Math", "Science", "English"]

# Step 3: Empty dictionary for marks
marks = {}

# Step 4: Input marks using loop
for subject in subjects:
    score = int(input(f"Enter marks for {subject}: "))
    marks[subject] = score

# Step 5: Calculate total
total = 0
for value in marks.values():
    total += value

# Step 6: Calculate average
average = total / len(marks)

# Step 7: Result using if/else
if average >= 40:
    result = "Pass"
else:
    result = "Fail"

# Step 8: Final output
print("Student:", name)
print("Marks:", marks)
print("Total:", total)
print("Average:", average)
print("Result:", result)'''

# try:
#     num = int(input("Enter number: "))
#     result = 10 / num

# except Exception as e:
#     print("Error:", e)

# else:
#     print("Result:", result)

# finally:
#     print("Program finished")

# class Student:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

# s1 = Student("Rahul", 20)

# print(s1.name)
# print(s1.age)

# class Student:
#     def __init__(self, name, marks):
#         self.name = name
#         self.marks = marks

#     def greet(self):
#         print("Hello,", self.name)

#     def result(self):
#         print("Marks:", self.marks)

# s1 = Student("Amit", 85)
# s1.greet()
# s1.result()

'''Only variables created with self are shared across methods'''


