import re

# Checking Password Strength Function
def check_password_strength(password):
    
    if len(password) < 8:
        return False
    
    if not any(char.isupper() for char in password):
        return False
    
    if not any(char.islower() for char in password):
        return False
    
    if not any(char.isdigit() for char in password):
        return False
    
    if not re.search(r"[!@#$%]", password):
        return False
    
    return True

# Getting User Input
password = input("Enter a password :- ")

# Calling function to check password strength
is_strong = check_password_strength(password)

if is_strong:
    print("Password is strong.")
else:
    print("Password is weak. Please choose a stronger password.")
