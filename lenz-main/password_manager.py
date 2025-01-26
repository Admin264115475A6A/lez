#573997
import json
import os
import getpass
import random
import string
import qrcode
import threading
from cryptography.fernet import Fernet, InvalidToken

class PasswordManager:
    def __init__(self, filename='passwords.json'):
        self.filename = filename
        self.key = self.load_key()
        self.cipher = Fernet(self.key)
        self.load_passwords()

    def load_key(self):
        """Load or generate a key for encryption."""
        try:
            if os.path.exists('secret.key'):
                with open('secret.key', 'rb') as key_file:
                    return key_file.read()
            else:
                key = Fernet.generate_key()
                with open('secret.key', 'wb') as key_file:
                    key_file.write(key)
                return key
        except IOError as e:
            print(f"Error loading or creating encryption key: {e}")
            exit(1)

    def load_passwords(self):
        """Load passwords from the JSON file with error handling."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    self.passwords = json.load(file)
                    # Decrypt passwords
                    for website in self.passwords:
                        try:
                            encrypted_password = self.passwords[website]['password']
                            self.passwords[website]['password'] = self.cipher.decrypt(encrypted_password.encode()).decode()
                        except InvalidToken:
                            print(f"Error decrypting password for {website}. Possibly corrupted data.")
                            self.passwords[website]['password'] = None  # Mark corrupted entries
            else:
                self.passwords = {}
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading passwords file: {e}")
            self.passwords = {}

    def save_passwords(self):
        """Save passwords to the JSON file, encrypting them."""
        try:
            encrypted_data = {}
            for website in self.passwords:
                encrypted_data[website] = {
                    'username': self.passwords[website]['username'],
                    'password': self.cipher.encrypt(self.passwords[website]['password'].encode()).decode()
                }
            with open(self.filename, 'w') as file:
                json.dump(encrypted_data, file, indent=4)
        except IOError as e:
            print(f"Error saving passwords: {e}")

    def add_password(self, website, username, password):
        """Add a new password."""
        self.passwords[website] = {'username': username, 'password': password}
        self.save_passwords()
        print(f'Password for {website} added successfully.')
        threading.Thread(target=self.create_qr_code, args=(website, username, password)).start()

    def retrieve_password(self, website):
        """Retrieve a password."""
        if website in self.passwords:
            if self.passwords[website]['password']:
                return self.passwords[website]
            else:
                print(f"The password for {website} is corrupted or unavailable.")
        else:
            print(f'No password found for {website}.')

    def delete_password(self, website):
        """Delete a password."""
        if website in self.passwords:
            del self.passwords[website]
            self.save_passwords()
            print(f'Password for {website} deleted successfully.')
        else:
            print(f'No password found for {website}.')

    def generate_password(self, length=12):
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def create_qr_code(self, website, username, password):
        """Create a QR code for the password entry."""
        try:
            data = f'Website: {website}\nUsername: {username}\nPassword: {password}'
            qr = qrcode.make(data)
            qr_filename = f'{website}_qr.png'
            qr.save(qr_filename)
            print(f'QR code saved as {qr_filename}.')
        except Exception as e:
            print(f"Error creating QR code: {e}")

def main():
    pm = PasswordManager()

    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. Retrieve Password")
        print("3. Delete Password")
        print("4. Generate Password")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            website = input("Enter website: ")
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            pm.add_password(website, username, password)

        elif choice == '2':
            website = input("Enter website: ")
            entry = pm.retrieve_password(website)
            if entry and entry['password']:
                print(f"Username: {entry['username']}, Password: {entry['password']}")

        elif choice == '3':
            website = input("Enter website: ")
            pm.delete_password(website)

        elif choice == '4':
            length = int(input("Enter password length (default is 12): ") or "12")
            generated_password = pm.generate_password(length)
            print(f"Generated Password: {generated_password}")
            pm.create_qr_code("Generated Password", "N/A", generated_password)

        elif choice == '5':
            print("Exiting Password Manager.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
