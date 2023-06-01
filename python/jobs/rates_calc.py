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


def inx(ear):
    print(f"--- earning {ear:.2f}")

    # put these numbers in a json file
    # get recent numbers; the ones used here are from 2022
    inx_cutoff = [11000, 18000, 31000, 60000, 90000, 1000000]
    inx_lvl = {
        11000: 0,
        18000: 20,
        31000: 35,
        60000: 42,
        90000: 48,
        1000000: 50,
        100000000: 55
    }
    inc = 0
    tax = 0
    calc_lvl = inx_cutoff[0]
    for i in inx_cutoff:
        next_idx = inx_cutoff.index(i)+1
        nextval = i if len(inx_cutoff) == next_idx else inx_cutoff[next_idx]
        # print(f"--- {ear}-{ear>i}({i})-{ear<=nextval}({nextval})")
        if ear > i and ear <= nextval:
            calc_lvl = nextval

    print(f"\n-- using calc lvl {calc_lvl} ({ear:.2f})")

    for i in inx_cutoff:
        if inx_lvl[i] == 0:
            inc = inc + i
        elif i <= calc_lvl:
            curr_tax_perc = inx_lvl[i]
            curr_idx = inx_cutoff.index(i)
            lastval = i if curr_idx == 0 else inx_cutoff[curr_idx - 1]
            curr_val = i if ear > i else ear
            curr_ear_range = curr_val-lastval
            tax_perc_val = (curr_ear_range/100)*curr_tax_perc
            tax = tax + tax_perc_val
            inc = inc + curr_ear_range - tax_perc_val
            print(f"--- curr_ear_range {curr_ear_range:.2f} - perc_val "
                  f"{tax_perc_val:.2f} - inc {inc:.2f} - tax {tax:.2f}")

    print(f"--- {inc:.2f}-{tax:.2f} = {inc-tax:.2f} ({(inc-tax)/12:.2f})")


def commission_income(earning=MAX_BASE_EARNING):
    hin = (earning / 100) * HEALTH_INSURANCE
    pin = (earning / 100) * PENSION_INSURANCE
    sep = (earning / 100) * SELF_EMPLOYED_PROVISION

    commission = hin + pin + sep + ACCIDENT_INSURANCE
    net_income = earning - commission

    print()
    print(f"\nCommission for income {earning:.2f}")
    print(f"-- monthly commission: {commission:.2f};\t\t net income: {net_income:.2f}")
    print(f"-- commission per annum: {commission * 12:.2f};\t net income: {net_income * 12:.2f}")

    inx(net_income * 12)


def income_table(base_month_sal, fixed_hour_rate):
    ref_month_sal = 5000
    if not base_month_sal:
        base_month_sal = ref_month_sal
    base_hours = 8
    base_days = 40
    ust = 0.2

    ref_inc_day = ref_month_sal/base_days
    ref_inc_hour = ref_inc_day/base_hours
    print(f"-- reference income/hour {ref_inc_hour:.2f};\t"
          f"ref income/day {ref_inc_day:.2f};\t"
          f"ref month salary: {ref_month_sal:.2f}")

    base_inc_day = base_month_sal/base_days
    base_inc_hour = base_inc_day/base_hours
    base_month_ust = base_month_sal*ust
    base_month_inc_ust = base_month_sal + base_month_ust
    print(f"-- base income/hour {base_inc_hour:.2f};\t"
          f"base income/day {base_inc_day:.2f};\t"
          f"base month salary: {base_month_sal:.2f};\t"
          f"base income/month+ust {base_month_inc_ust:.2f}({base_month_ust:.2f})")

    if not fixed_hour_rate:
        fixed_hour_rate = 16

    inc_day = fixed_hour_rate*base_hours
    inc_month = inc_day*base_days
    month_ust = inc_month*ust
    inc_month_ust = inc_month + month_ust
    print(f"-- fixed income/hour {fixed_hour_rate:.2f};\t"
          f"fixed income/day {inc_day:.2f};\t"
          f"fixed income/month {inc_month:.2f};\t"
          f"fixed income/month+ust {inc_month_ust:.2f}({month_ust:.2f})")


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-e", "--earning", type=int, required=False,
                        help="Provide monthly income in euro")
    parser.add_argument("-r", "--rate", type=float, required=False,
                        help="Provide hourly rates in euro")
    args = parser.parse_args()

    income_table(args.earning, args.rate)

    commission_income()

    if args.earning:
        commission_income(args.earning)


if __name__ == "__main__":
    run()
