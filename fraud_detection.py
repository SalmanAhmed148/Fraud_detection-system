import mysql.connector
import random

# Database connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lost",
    database="fraud_detection"
)

def generate_unique_user_id():
    # Generate a unique 6-digit user ID (you can adjust the length)
    while True:
        user_id = ''.join(random.choice('0123456789') for _ in range(6))
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        existing_user = cursor.fetchone()
        if not existing_user:
            return user_id

def create_user(username, email, pin):
    cursor = db.cursor()

    # Generate a unique user ID
    user_id = generate_unique_user_id()

    # Insert the new user into the database with a balance of 0.00
    insert_user = "INSERT INTO users (id, username, email, pin, balance) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_user, (user_id, username, email, pin, 0.00))
    db.commit()

    print(f"User created successfully! Your unique user ID is: {user_id}")
    print("Please use this ID for transactions and transaction history.")

def deposit(user_id, amount):
    cursor = db.cursor()

    # Update the user's balance
    cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, user_id))
    db.commit()

    # Check for potential fraud
    if amount > 1000.00:  # Adjust the threshold as needed
        # Log a fraud alert
        insert_alert = "INSERT INTO fraud_alerts (user_id, transaction_id, reason) VALUES (%s, %s, %s)"
        cursor.execute(insert_alert, (user_id, 0, "Transaction exceeded threshold"))  # Adjust the transaction_id as needed
        db.commit()
        print("Potential fraud transaction detected. Alert logged.")

    print("Deposit completed successfully.")

def withdrawal(user_id, amount):
    cursor = db.cursor()

    # Check if the user has sufficient balance
    cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
    user_balance = cursor.fetchone()[0]

    if user_balance < amount:
        print("Insufficient balance.")
        return

    # Update the user's balance
    cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, user_id))
    db.commit()

    print("Withdrawal completed successfully.")

def view_transaction(user_id):
    cursor = db.cursor()

    # Retrieve and display the user's transaction history
    cursor.execute("SELECT id, amount, timestamp, transaction_type FROM transactions WHERE user_id = %s", (user_id,))
    transactions = cursor.fetchall()

    if not transactions:
        print("No transaction history found.")
    else:
        print("Transaction History:")
        print("ID\tAmount\tTimestamp\tTransaction Type")
        for transaction in transactions:
            print(f"{transaction[0]}\t${transaction[1]:.2f}\t{transaction[2]}\t{transaction[3]}")

def make_transaction(user_id):
    while True:
        print("\nTransaction Options:")
        print("1. Deposit")
        print("2. Withdrawal")
        print("3. Back to Main Menu")
        choice = input("Select a transaction option: ")

        if choice == "1":
            amount = float(input("Enter the deposit amount: "))
            if amount <= 0:
                print("Invalid amount. Please enter a positive amount.")
            else:
                deposit(user_id, amount)
        elif choice == "2":
            amount = float(input("Enter the withdrawal amount: "))
            if amount <= 0:
                print("Invalid amount. Please enter a positive amount.")
            else:
                withdrawal(user_id, amount)
        elif choice == "3":
            break
        else:
            print("Invalid option. Please select a valid transaction option.")


def track_longitude_latitude(user_id, longitude, latitude):
    cursor = db.cursor()

    # Insert longitude and latitude into a new table (for illustration purposes)
    insert_location = "INSERT INTO location_data (user_id, longitude, latitude) VALUES (%s, %s, %s)"
    cursor.execute(insert_location, (user_id, longitude, latitude))
    db.commit()

    print("Longitude and latitude data recorded.")

def user_profile(user_id):
    while True:
        print("\nUser Profile:")
        print("1. View Profile")
        print("2. Change Password")
        print("3. Change Email")
        print("4. Change Name")
        print("5. Back to Main Menu")
        choice = input("Select an option: ")

        cursor = db.cursor()

        if choice == "1":
            # View user profile information
            cursor.execute("SELECT id, username, email, balance FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                print(f"User ID: {user_data[0]}")
                print(f"Username: {user_data[1]}")
                print(f"Email: {user_data[2]}")
                print(f"Balance: ${user_data[3]:.2f}")
            else:
                print("User not found.")
        elif choice == "2":
            # Change Password
            pin = input("Enter your 4-digit PIN: ")
            cursor.execute("SELECT pin FROM users WHERE id = %s", (user_id,))
            stored_pin = cursor.fetchone()
            if stored_pin and pin == stored_pin[0]:
                new_pin = input("Enter a new 4-digit PIN: ")
                cursor.execute("UPDATE users SET pin = %s WHERE id = %s", (new_pin, user_id))
                db.commit()
                print("PIN updated successfully.")
            else:
                print("Incorrect PIN. Access denied.")
            pass
        elif choice == "3":
            # Change Email
            pin = input("Enter your 4-digit PIN: ")
            cursor.execute("SELECT pin FROM users WHERE id = %s", (user_id,))
            stored_pin = cursor.fetchone()
            if stored_pin and pin == stored_pin[0]:
                new_email = input("Enter a new email address: ")
                cursor.execute("UPDATE users SET email = %s WHERE id = %s", (new_email, user_id))
                db.commit()
                print("Email address updated successfully.")
            else:
                print("Incorrect PIN. Access denied.")
            pass
        elif choice == "4":
            # Change Name (Username)
            pin = input("Enter your 4-digit PIN: ")
            cursor.execute("SELECT pin FROM users WHERE id = %s", (user_id,))
            stored_pin = cursor.fetchone()
            if stored_pin and pin == stored_pin[0]:
                new_username = input("Enter a new username: ")
                cursor.execute("UPDATE users SET username = %s WHERE id = %s", (new_username, user_id))
                db.commit()
                print("Username updated successfully.")
            else:
                print("Incorrect PIN. Access denied.")
            pass
        elif choice == "5":
            break
        else:
            print("Invalid option. Please select a valid option.")

def send_money(sender_id, receiver_id, amount):
    cursor = db.cursor()

    # Check if sender and receiver exist
    cursor.execute("SELECT id FROM users WHERE id = %s", (sender_id,))
    sender_exists = cursor.fetchone()
    cursor.execute("SELECT id FROM users WHERE id = %s", (receiver_id,))
    receiver_exists = cursor.fetchone()

    if not sender_exists or not receiver_exists:
        print("Sender or receiver does not exist.")
        return

    # Check if sender has sufficient balance
    cursor.execute("SELECT balance FROM users WHERE id = %s", (sender_id,))
    sender_balance = cursor.fetchone()[0]

    if sender_balance < amount:
        print("Sender has insufficient balance.")
        return

    # Update sender's balance
    cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, sender_id))
    # Update receiver's balance
    cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, receiver_id))

    # Record the transaction
    insert_transaction = "INSERT INTO transactions (user_id, amount, transaction_type) VALUES (%s, %s, %s)"
    cursor.execute(insert_transaction, (sender_id, -amount, "transfer"))
    cursor.execute(insert_transaction, (receiver_id, amount, "transfer"))

    db.commit()

    print("Money sent successfully.")


def main():
    while True:
        print("\nOptions:")
        print("1. Create User")
        print("2. Make Transaction")
        print("3. View Transaction History")
        print("4. User Profile")
        print("5. Send Money")
        print("6. Exit")
        choice = input("Select an option: ")

        cursor = db.cursor()

        if choice == "1":
            username = input("Enter your username: ")
            email = input("Enter your email: ")
            pin = input("Enter your 4-digit PIN: ")
            create_user(username, email, pin)
        elif choice == "2":
            user_id = input("Enter your unique user ID: ")
            make_transaction(user_id)  # Placeholder function name, should be replaced with actual transaction function
        elif choice == "3":
            user_id = input("Enter your unique user ID: ")
            view_transaction(user_id)
        elif choice == "4":
            user_id = input("Enter your unique user ID: ")
            user_profile(user_id)
        elif choice == "5":
            sender_id = input("Enter your unique user ID as sender: ")
            receiver_id = input("Enter the receiver's unique user ID: ")
            amount = float(input("Enter transaction amount: "))
            send_money(sender_id, receiver_id, amount)
        elif choice == "6":
            break
        else:
            print("Invalid option. Please select a valid option.")

if __name__ == "__main__":
    main()
