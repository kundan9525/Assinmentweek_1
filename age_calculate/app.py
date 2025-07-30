from datetime import datetime

def get_birthdate():
    while True:
        user_input = input("Enter your birth date (mm/dd/yyyy): ")
        try:
            # Step 1: Parse the input string
            birth_date = datetime.strptime(user_input, "%m/%d/%Y")
            return birth_date
        except ValueError:
            print("Invalid format or invalid date. Please use mm/dd/yyyy format.")

def calculate_age(birth_date):
    today = datetime.today()
    age = today.year - birth_date.year
    # Adjust if birthday hasn't occurred yet this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

def main():
    print("Welcome to the Birthdate Analyzer \n")
    
    birth_date = get_birthdate()
    age = calculate_age(birth_date)
    
    # Display outputs
    print("\nValid birthdate entered!")
    print(f"European format: {birth_date.strftime('%d/%m/%Y')}")
    print(f"You are {age} years old.")

if __name__ == "__main__":
    main()
