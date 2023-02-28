def run():
    years = 5
    gogreen = 3.11
    online = 2.22
    month = years*12
    for i in range(month):
        currval = i+1
        greenval = (currval-12)*gogreen
        if greenval < 0:
            greenval = 0
        print(f"Month {currval}: online {currval*online:.2f} gogreen {greenval:.2f}")


if __name__ == "__main__":
    run()
