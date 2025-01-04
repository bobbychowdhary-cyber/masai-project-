import os
import hashlib
from datetime import datetime

class BankingSystem:
    ACCOUNTS_FILE = "accounts.txt"

    def __init__(self):
        self.current_user = None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save_account(self, account_number, name, hashed_password, balance):
        with open(self.ACCOUNTS_FILE, "a") as file:
            file.write(f"{account_number},{name},{hashed_password},{balance}\n")

    def find_account(self, account_number, password):
        if not os.path.exists(self.ACCOUNTS_FILE):
            return None
        with open(self.ACCOUNTS_FILE, "r") as file:
            for line in file:
                acc_num, name, hashed_password, balance = line.strip().split(",")
                if acc_num == account_number and hashed_password == self.hash_password(password):
                    return {"account_number": acc_num, "name": name, "balance": float(balance)}
        return None

    def update_balance(self):
        accounts = []
        with open(self.ACCOUNTS_FILE, "r") as file:
            accounts = file.readlines()
        with open(self.ACCOUNTS_FILE, "w") as file:
            for line in accounts:
                acc_num, name, hashed_password, balance = line.strip().split(",")
                if acc_num == self.current_user["account_number"]:
                    file.write(f"{acc_num},{name},{hashed_password},{self.current_user['balance']}\n")
                else:
                    file.write(line)

    def create_account(self):
        name = input("Enter your name: ")
        try:
            balance = float(input("Initial deposit: "))
            if balance < 0: raise ValueError("Deposit must be positive.")
        except ValueError as e:
            print(e); return
        account_number = datetime.now().strftime("%Y%m%d%H%M%S")
        password = self.hash_password(input("Set your password: "))
        self.save_account(account_number, name, password, balance)
        print(f"Account created. Number: {account_number}")

    def login(self):
        account_number = input("Account number: ")
        password = input("Password: ")
        user = self.find_account(account_number, password)
        if user:
            self.current_user = user
            print(f"Welcome, {user['name']}!")
            return True
        print("Invalid credentials.")
        return False

    def deposit(self):
        try:
            amount = float(input("Deposit amount: "))
            if amount <= 0: raise ValueError("Amount must be positive.")
            self.current_user["balance"] += amount
            self.update_balance()
            print(f"Deposited. New balance: {self.current_user['balance']}")
        except ValueError as e:
            print(e)

    def withdraw(self):
        try:
            amount = float(input("Withdraw amount: "))
            if amount <= 0: raise ValueError("Amount must be positive.")
            if amount > self.current_user["balance"]: raise ValueError("Insufficient funds.")
            self.current_user["balance"] -= amount
            self.update_balance()
            print(f"Withdrawn. New balance: {self.current_user['balance']}")
        except ValueError as e:
            print(e)

    def check_balance(self):
        print(f"Current balance: {self.current_user['balance']}")

    def user_menu(self):
        options = {"1": self.deposit, "2": self.withdraw, "3": self.check_balance}
        while True:
            print("1. Deposit\n2. Withdraw\n3. Check Balance\n4. Logout")
            choice = input("Enter choice: ")
            if choice == "4": break
            action = options.get(choice)
            if action: action()
            else: print("Invalid choice.")

    def main_menu(self):
        while True:
            print("1. Create Account\n2. Login\n3. Exit")
            choice = input("Enter choice: ")
            if choice == "1": self.create_account()
            elif choice == "2" and self.login(): self.user_menu()
            elif choice == "3": break
            else: print("Invalid choice.")

if __name__ == "__main__":
    BankingSystem().main_menu() 
    