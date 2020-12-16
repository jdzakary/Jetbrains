import math
import argparse

parser = argparse.ArgumentParser(description='Calculate a loan')
# Required Arguments that must be entered
parser.add_argument("--type", choices=['diff', 'annuity'], help="Indicate which type of loan you are calculating")
parser.add_argument("--interest", type=float)

# Work for both types of loans
parser.add_argument("--principal", type=int)
parser.add_argument("--periods", type=int)

# Only works for annuity loans
parser.add_argument("--payment", type=int)

# There are no command line options that only work for diff loans.
# The diff loan options are always the same 4. Only annuity has variability

args = parser.parse_args()

# Check for required parameters
if args.type is None:
    print("Incorrect parameters")
    exit()
if args.interest is None:
    print("Incorrect parameters")
    exit()

# Check the number of parameters provided
args_2 = vars(args)
args_3 = args_2.values()
x = 0
for item in args_3:
    if item is None:
        x += 1

if x != 1:
    print("Incorrect parameters")
    exit()

# Check for negative parameters
if args.interest < 0:
    print("Incorrect parameters")
if args.payment is not None:
    if args.payment < 0:
        print("Incorrect parameters")
        exit()
if args.periods is not None:
    if args.periods < 0:
        print("Incorrect parameters")
        exit()
if args.principal is not None:
    if args.principal < 0:
        print("Incorrect parameters")
        exit()

# Calculate the interest rate
i = args.interest / 1200

# Calculate the differential loan
if args.type == 'diff':
    if args.payment is not None:
        print("Incorrect parameters")
        exit()
    m = 1
    n = args.periods
    p = args.principal
    total = 0
    while m <= n:
        d = math.ceil(p/n + i*(p - p*(m-1)/n))
        print("Month " + str(m) + ": payment is " + str(d))
        m += 1
        total += d
    overpay = total - p
    print()
    print("Overpayment = ", overpay)
    exit()

# Calculate the annuity loan
if args.type == 'annuity':
    if args.payment is None:
        p = args.principal
        n = args.periods
        A = p * i * math.pow(1+i, n) / (math.pow(1+i, n) - 1)
        print("Your annuity payment = " + str(math.ceil(A)) + "!")
        overpay = math.ceil(A) * n - p
        print("Overpayment =", math.ceil(overpay))
    if args.principal is None:
        A = args.payment
        n = args.periods
        p = A * (math.pow(1+i, n) - 1) / i / math.pow(1+i, n)
        p = math.floor(p)
        print("Your loan principal = " + str(p) + "!")
        overpay = A * n - p
        print("Overpayment =", overpay)
    if args.periods is None:
        A = args.payment
        p = args.principal
        n = math.log(A/(A-i*p), 1+i)
        n = math.ceil(n)
        years = math.floor(n/12)
        months = n - 12*years
        if months == 0:
            print("It will take " + str(years) + " to repay this loan!")
        elif years == 0:
            print("It will take " + str(months) + " to repay this loan!")
        else:
            print("It will take " + str(years) + " years and " + str(months) + " months to repay this loan!")
        overpay = n * A - p
        print("Overpayment =", overpay)
