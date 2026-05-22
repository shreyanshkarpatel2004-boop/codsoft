import random
import string


def get_password_length():
    while True:
        length_input = input("Enter the desired password length: ")
        if not length_input.isdigit():
            print("Please enter a valid positive number.")
            continue

        length = int(length_input)
        if length < 6:
            print("For security, please choose a length of at least 6 characters.")
            continue

        return length


def generate_password(length):
    characters = (
        string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits
        + string.punctuation
    )

    # Ensure at least one character of each type is included
    password_chars = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation),
    ]

    password_chars.extend(random.choice(characters) for _ in range(length - len(password_chars)))
    random.shuffle(password_chars)

    return "".join(password_chars)


def main():
    print("Password Generator")
    print("Create a strong, random password with letters, digits, and symbols.")

    length = get_password_length()
    password = generate_password(length)

    print(f"\nGenerated password ({length} chars):")
    print(password)


if __name__ == "__main__":
    main()
