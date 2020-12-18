import random
import sqlite3

random.seed()
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


def create_random(digits):
    counter = 0
    number = ''
    while counter < digits:
        number = number + str(random.randrange(10))
        counter += 1
    return number


def check_balance(number):
    cur.execute('SELECT balance FROM card WHERE number = ' + number + ';')
    balance = cur.fetchall()
    return balance[0][0]


def add_money(number, money):
    new_balance = int(check_balance(number)) + int(money)
    cur.execute('UPDATE card SET balance = '+str(new_balance)+' WHERE number = '+number+';')
    conn.commit()


def remove_money(number, money):
    new_balance = int(check_balance(number)) - int(money)
    cur.execute('UPDATE card SET balance = '+str(new_balance)+' WHERE number = '+number+';')
    conn.commit()


def validate_card(card):
    position = 1
    total = 0
    card = str(card)
    for digit in card:
        if position % 2 != 0:
            digit = int(digit) * 2
        if int(digit) > 9:
            digit = int(digit) - 9
        total += int(digit)
        position += 1
    difference = 10 - (total % 10)
    if difference == 10:
        check_sum = 0
    else:
        check_sum = difference
    return str(check_sum)


def check_card(number):
    cur.execute('SELECT number FROM card WHERE number = ' + number + ';')
    return len(cur.fetchall())


def check_pin(number, pin):
    cur.execute('SELECT number FROM card WHERE number = '+number+' AND pin = '+pin+';')
    return len(cur.fetchall())


def create_account():
    user_id = create_random(9)
    number = '400000' + user_id
    number = '400000' + user_id + validate_card(number)
    pin = create_random(4)
    if check_card(number) == 0:
        print("Your card has been created")
        print("Your card number:")
        print(number)
        print("Your card PIN:")
        print(pin)
        cur.execute('INSERT INTO card (number, pin) VALUES (' + number + ',' + pin + ');')
        conn.commit()
    else:
        create_account()


def terminate_account(number):
    cur.execute('DELETE FROM card WHERE number = ' + number + ';')
    conn.commit()


def transfer_money(start):
    print("Enter card number:")
    target = input()
    balance = check_balance(start)
    last_digit = target[-1]
    modified_target = target[0:15]
    if last_digit != validate_card(modified_target):
        print("Probably you made a mistake in the card number. Please try again!")
        print()
        account()
    elif check_card(target) != 1:
        print("Such a card does not exist.")
        print()
        account()
    else:
        print("Enter how much money you want to transfer:")
        amount = input()
        if int(amount) > int(balance):
            print("Not enough money!")
            print()
            account()
        else:
            add_money(target, amount)
            remove_money(start, amount)
            print("Success!")
            print()
            account()


def home():
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    action = int(input())
    print()
    if action == 1:
        create_account()
        print()
        home()
    elif action == 2:
        login()
    elif action == 0:
        print("Bye!")
        exit()


def login():
    print("Enter your card number:")
    number = input()
    print("Enter your pin:")
    pin = input()
    print()
    if check_card(number) > 0:
        if check_pin(number, pin) == 1:
            print("You have successfully logged in!")
            global current_user
            current_user = number
            print()
            account()
        else:
            print("Wrong card number or PIN!")
            print()
            home()
    else:
        print("Wrong card number or PIN!")
        print()
        home()


def account():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")
    action = int(input())
    print()
    if action == 1:
        print(check_balance(current_user))
        print()
        account()
    if action == 2:
        print("Enter income:")
        add_money(current_user, input())
        print("Income was added!")
        print()
        account()
    if action == 3:
        transfer_money(current_user)
    if action == 4:
        terminate_account(current_user)
        print("The account has been closed!")
        print()
        home()
    if action == 5:
        print("You have successfully logged out!")
        print()
        home()
    if action == 0:
        print("Bye!")
        exit()


home()
