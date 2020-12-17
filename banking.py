import random

random.seed()
existing_ids = []
cards = dict()


def create_random(digits):
    counter = 0
    number = ''
    while counter < digits:
        number = number + str(random.randrange(10))
        counter += 1
    return number


def create_account():
    user_id = create_random(9)
    while user_id in existing_ids:
        user_id = create_random(9)
    number = '400000' + user_id + create_random(1)
    existing_ids.append(user_id)
    pin = create_random(4)
    cards[number] = pin
    print("Your card has been created")
    print("Your card number:")
    print(number)
    print("Your card PIN:")
    print(pin)


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
    if number in cards:
        if pin == cards[number]:
            print("You have successfully logged in!")
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
    print("2. Log out")
    print("0. Exit")
    action = int(input())
    print()
    if action == 1:
        print("Balance: 0")
        print()
        account()
    elif action == 2:
        print("You have successfully logged out!")
        print()
        home()
    elif action == 0:
        print("Bye!")
        exit()


home()
