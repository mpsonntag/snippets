def run():
    years = 10
    gogreen = 3.11
    online = 2.22
    month = years*12
    currval = 0
    greenval = 0
    for i in range(month):
        currval = i+1
        greenval = (currval-12)*gogreen
        if greenval < 0:
            greenval = 0
        print(f"Month {currval}: online {currval*online:.2f} gogreen {greenval:.2f}")

    print(f"\n-- Final rates after {years} years")
    print(f"-- Month {currval}: online {currval*online:.2f} gogreen {greenval:.2f}")
    print(f"-- gogreen final expenses: {greenval-currval*online:.2f}")


if __name__ == "__main__":
    run()
