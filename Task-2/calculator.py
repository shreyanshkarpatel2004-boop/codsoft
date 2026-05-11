def get_number(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_operation():
    print("Choose an operation:")
    print("1 - Add (+)")
    print("2 - Subtract (-)")
    print("3 - Multiply (*)")
    print("4 - Divide (/)")

    while True:
        choice = input("Enter the operation number (1-4): ")
        if choice in {"1", "2", "3", "4"}:
            return choice
        print("Invalid choice. Please enter 1, 2, 3, or 4.")


def calculate(a, b, operation):
    if operation == "1":
        return a + b
    if operation == "2":
        return a - b
    if operation == "3":
        return a * b
    if operation == "4":
        if b == 0:
            return None
        return a / b


def main():
    print("Simple Calculator")
    number1 = get_number("Enter the first number: ")
    number2 = get_number("Enter the second number: ")
    operation = get_operation()

    result = calculate(number1, number2, operation)

    if result is None:
        print("Error: Division by zero is undefined.")
        return

    symbols = {"1": "+", "2": "-", "3": "*", "4": "/"}
    symbol = symbols[operation]
    print(f"{number1} {symbol} {number2} = {result}")


if __name__ == "__main__":
    main()
