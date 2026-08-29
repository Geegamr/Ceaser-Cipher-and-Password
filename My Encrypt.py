import random

base_seed = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+-=~`[]{}|;:',.<>/?"


def get_custom_seed(password):
    #Generates a deterministic shuffled seed based on a password.
    seed_list = list(base_seed)
    random.seed(password)
    random.shuffle(seed_list)
    return "".join(seed_list)


def encrypt(text, shift, password):
    seed = get_custom_seed(password)
    seed_len = len(seed)
    index = {c: i for i, c in enumerate(seed)}
    encrypted_text = []
    for char in text:
        i = index.get(char.lower())
        if i is not None:
            c = seed[(i + shift) % seed_len]
            encrypted_text.append(c.upper() if char.isupper() else c)
        else:
            encrypted_text.append(char)
    return "".join(encrypted_text)


def decrypt(text, shift, password):
    seed = get_custom_seed(password)
    seed_len = len(seed)
    index = {c: i for i, c in enumerate(seed)}
    decrypted_text = []
    for char in text:
        i = index.get(char.lower())
        if i is not None:
            c = seed[(i - shift) % seed_len]
            decrypted_text.append(c.upper() if char.isupper() else c)
        else:
            decrypted_text.append(char)
    return "".join(decrypted_text)


def get_seed():
    #Ask for a password and print the seed it turns into.
    password = input("\nEnter a password: ").strip()
    print("\nBase seed:")
    print(" ", base_seed)
    print("\nSeed for that password:")
    print(" ", get_custom_seed(password))


def read_text_file(filepath):
    #Read the full contents of a text file.
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_text_file(filepath, content):
    #Write content to a text file.
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def encrypt_file(filepath, shift, password):
    #Encrypt the contents of a text file in place, then return the new text.
    content = read_text_file(filepath)
    encrypted = encrypt(content, shift, password)
    write_text_file(filepath, encrypted)
    return encrypted


def decrypt_file(filepath, shift, password):
    #Decrypt the contents of a text file in place, then return the new text.
    content = read_text_file(filepath)
    decrypted = decrypt(content, shift, password)
    write_text_file(filepath, decrypted)
    return decrypted


def prompt_for_file(operation_name):
    #Collect file, shift, and password, then run encrypt or decrypt on the file.
    while True:
        try:
            user_input = input("Enter file path, shift, and password (notes.txt, 3, secret123): ")
            parts = [p.strip() for p in user_input.rsplit(",", 2)]
            if len(parts) != 3:
                raise ValueError()
            filepath = parts[0]
            shift = int(parts[1])
            password = parts[2]
            break
        except ValueError:
            print("\nInvalid format. Please use 'File Path, Shift, Password' (notes.txt, 3, secret123).")

    try:
        if operation_name == "encrypt":
            encrypt_file(filepath, shift, password)
        else:
            decrypt_file(filepath, shift, password)
        print(f"\n{operation_name.capitalize()}ed and overwrote: {filepath}")
        print(f"Saved with shift={shift}, password={password}.")
    except FileNotFoundError:
        print(f"\nFile not found: {filepath}")
    except PermissionError:
        print(f"\nPermission denied reading/writing: {filepath}")
    except Exception as e:
        print(f"\nAn error occurred while {operation_name}ing the file: {e}")


def main():
    while True:
        print("\nChoose an option:")
        print("[1]. Encrypt text")
        print("[2]. Decrypt text")
        print("[3]. Encrypt a text file")
        print("[4]. Decrypt a text file")
        print("[5]. Get seed from password")
        print("[6]. Exit")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1" or choice.lower() == "/en":
            while True:
                try:
                    user_input = input("Enter text, shift, and password (Hello, 3, secret123): ")
                    parts = [p.strip() for p in user_input.rsplit(",", 2)]
                    if len(parts) != 3:
                        raise ValueError()
                    text = parts[0]
                    shift = int(parts[1])
                    password = parts[2]
                    break
                except ValueError:
                    print("\nInvalid format. Please use 'Text, Shift, Password' (Hello, 3, secret123).")

            encrypted = encrypt(text, shift, password)
            print(f"\nResult: {encrypted}, {shift}, {password}")

        elif choice == "2" or choice.lower() == "/de":
            while True:
                try:
                    user_input = input("Enter text, shift, and password (K#$oo, 3, secret123): ")
                    parts = [p.strip() for p in user_input.rsplit(",", 2)]
                    if len(parts) != 3:
                        raise ValueError()
                    text = parts[0]
                    shift = int(parts[1])
                    password = parts[2]
                    break
                except ValueError:
                    print("\nInvalid format. Please use 'Text, Shift, and Password' (K#$oo, 3, secret123).")

            print("\nDecrypted text:", decrypt(text, shift, password))

        elif choice == "3" or choice.lower() == "/ef":
            prompt_for_file("encrypt")

        elif choice == "4" or choice.lower() == "/df":
            prompt_for_file("decrypt")

        elif choice == "5" or choice.lower() == "/seed":
            get_seed()

        elif choice == "6" or choice.lower() == "/e":
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
