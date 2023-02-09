"""
numbers based on https://www.wko.at/service/arbeitsrecht-sozialrecht/Neue_Selbststaendige_einfach.html

NOTE: base earning should be higher since there is no 13th salary...
"""

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

    print(f"Commission for income {earning:.2f}")
    print(f"-- monthly commission: {commission:.2f};\t\t net income: {net_income:.2f}")
    print(f"-- commission per annum: {commission * 12:.2f};\t net income: {net_income * 12:.2f}")


commission_income()

commission_income(3000)
