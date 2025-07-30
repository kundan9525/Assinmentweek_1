def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive integer.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

def main():
    print("Prime Number Finder")

    # Input and validation
    start = get_positive_integer("Enter the start of the range: ")
    end = get_positive_integer("Enter the end of the range: ")

    if start > end:
        print("Start of range cannot be greater than end. Swapping values.")
        start, end = end, start

    # Find prime numbers
    primes = [num for num in range(start, end + 1) if is_prime(num)]

    # Display results
    print(f"\nPrime numbers between {start} and {end}:")

    for i, prime in enumerate(primes, 1):
        print(f"{prime:5}", end="\n" if i % 10 == 0 else "")
    
    if not primes:
        print("No prime numbers found in the given range.")
    else:
        print("\nDone.")

if __name__ == "__main__":
    main()
