num1 = int(input("Enter the first number :"))
num2 = int(input("Enter the second number:"))

print(f"The sum of {num1}) and {num2} is: {num1 + num2}")
print(f"The difference between {num1} is: {num2} is: {num1 - num2}")
print(f"The product of {num1} and {num2} is: {num1 * num2}")
print(f"The quotient of {num1} and {num2} is: {num1 / num2}")


# function to check if a student has passed or failed based on marks 
def check_pass_fail(marks):
    if marks >= 50:
        return "passed"
    else:
        return "failed"
    