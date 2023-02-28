"""
numbers based on https://www.wko.at/service/arbeitsrecht-sozialrecht/Neue_Selbststaendige_einfach.html

NOTE: base earning should be higher since there is no 13th salary...

income_tax still missing
"""
import argparse

# absolute
MAX_BASE_EARNING = 6615

# percentage
HEALTH_INSURANCE = 6.80

# percentage
PENSION_INSURANCE = 18.5

# percentage
SELF_EMPLOYED_PROVISION = 1.53

# absolute
ACCIDENT_INSURANCE = 10.64


def commission_income(earning=MAX_BASE_EARNING):
    hin = (earning / 100) * HEALTH_INSURANCE
    pin = (earning / 100) * PENSION_INSURANCE
    sep = (earning / 100) * SELF_EMPLOYED_PROVISION

    commission = hin + pin + sep + ACCIDENT_INSURANCE
    net_income = earning - commission

    print()
    print(f"Commission for income {earning:.2f}")
    print(f"-- monthly commission: {commission:.2f};\t\t net income: {net_income:.2f}")
    print(f"-- commission per annum: {commission * 12:.2f};\t net income: {net_income * 12:.2f}")


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-e", "--earning", type=int, required=False, help="Provide income in euro")
    args = parser.parse_args()

    commission_income()

    if args.earning:
        commission_income(args.earning)


if __name__ == "__main__":
    run()
