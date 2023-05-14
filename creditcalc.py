import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--type")
parser.add_argument("--principal", type=float)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
parser.add_argument("--payment", type=float)
args = parser.parse_args()

if (args.type != "diff" and args.type != "annuity" or args.interest is None):
    print("Incorrect parameters. --type can be 'diff' or 'annuity'. --interest is mandatory")
    exit(-1)

nominal_rate = args.interest / 12 / 100


if args.type == "diff":
    if args.principal is None or args.periods is None or args.payment is not None:
        print("Missing required argument. Need to specify --principal and --periods, if using type='diff'.")
        exit(-1)
    count = 0
    overpayment = 0
    for count in range(args.periods):
        count += 1
        installment = math.ceil(args.principal / args.periods + nominal_rate * (args.principal - (args.principal * (count - 1)) / args.periods))
        overpayment += installment
        print(f"Period {count}: payment is {installment}")
    print(f"Overpayment: {overpayment - args.principal}")
elif args.payment is None:
    annuity_payment = math.ceil(
        args.principal * nominal_rate * (1 + nominal_rate) ** args.periods / ((1 + nominal_rate) ** args.periods - 1))
    overpayment = math.ceil(annuity_payment * args.periods - args.principal)
    print(f"Your annuity payment = {annuity_payment}")
    print(f"Overpayment = {overpayment}")
elif args.periods is None:
    months_to_repayment = math.ceil(
        math.log((args.payment / (args.payment - nominal_rate * args.principal)), (nominal_rate + 1)))
    overpayment = math.ceil(months_to_repayment * args.payment - args.principal)
    if months_to_repayment <= 1:
        print(f'It will take {months_to_repayment} month to repay the loan')
    elif months_to_repayment < 12:
        print(f'It will take {months_to_repayment} months to repay the loan')
    else:
        months_to_years = months_to_repayment // 12
        left_months = months_to_repayment % 12
        if months_to_years == 1:
            print(f'It will take {months_to_years} year to repay this loan!')
        elif left_months == 0:
            print(f'It will take {months_to_years} years to repay this loan!')
        else:
            print(f'It will take {months_to_years} years and {left_months} months to repay this loan!')
    print(f"Overpayment = {overpayment}")
elif args.principal is None:
    loan_principal = math.floor(
        args.payment / ((nominal_rate * (1 + nominal_rate) ** args.periods) / ((1 + nominal_rate) ** args.periods - 1)))
    print(f'Your loan principal = {loan_principal}!')
    overpayment = math.ceil(args.payment * args.periods - loan_principal)
    print(f"Overpayment = {overpayment}")
