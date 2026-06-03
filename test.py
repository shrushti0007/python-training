 # 1 student -5 varaibles
student_name = "shrushti"
student_marks =85
student_roll_number =55
student_subject ="java"
student_city ="Hingoli"


#list
student = ["shrushti", "akashara","durga","sai"]
marks = [ 85, 92, 78, 90]
roll_number = [62, 13, 12, 10]
subjects = ["java", "python", "c++", "javascript"]
citites =["Hingoli", "pune","mumbai", "nagapur"]

#get roll number of akashara
# rolls[1] -> 13

solution = {"name": "shrushti", "marks": 85, "age": 20}
#Dictionary - key: value pair

student = {
    "name": "shrushti",
    "marks": 85,
    "roll_number": 55,
    "subject": "java",
    "city": "hingoli"
}

# Accessing values from the dictionary
print(student["name"]) # output: shrushti
print(student["marks"]) # output; 85
print(student["roll_number"]) # output: 55
print(student["subject"]) # output: java
print(student["city"]) # output: hingoli

#update values in dictionary
student["marks"] =90
print(student["marks"]) # output: 90

# New field 
student ["grade"] = "A"
print(student["grade"]) # output: A

# Check
print ("name" in student) # output: True
print("age" in student) # output: False

# keys and values
print(student.keys()) # output: dict_keys(['name', 'marks', 'roll_no],
print(student.values()) # output: dict_values
