import hashlib

print(hashlib.sha1(b"abcdefg@cd").hexdigest())


# kwargs example
def conditional_print(filename, local_style=True, custom_template=None):
    print(f"filename: {filename}, local_style: {local_style}, custom_template: {custom_template}")


def handle_kwargs(filename, **kwargs):
    local_style = False
    custom_template = None

    if "local_style" in kwargs and isinstance(kwargs["local_style"], bool):
        local_style = kwargs["local_style"]
    if "custom_template" in kwargs and isinstance(kwargs["custom_template"], str):
        custom_template = kwargs["custom_template"]
    conditional_print(filename, local_style, custom_template)


def scale_print(add_trips=0):
    v_card = 60
    vie_day = 10
    curr = 1440 + 120 + v_card
    pot = 949 + 600
    pot_reg = 1095 + 600
    if not add_trips:
        print(f"Current: {curr}\tklimaticket: {pot}/{pot_reg}")
    for i in range(add_trips):
        curr_add = i * (120 + vie_day)
        pot_add = i * 50
        print(f"Current: {curr + curr_add}\tklimaticket: {pot + pot_add}/{pot_reg + pot_add}\t"
              f"add trip {i}")

    x2017 = 44.00 + 59.90 + 44.00 + 69.90 + 44.00 + 69.90 + 49.90 + 44.00 + 58.40 + 58.40 + \
            58.40 + 79.90 + 44.00 + 44.00 + 58.40 + 58.40 + 58.40 + 44.00 + (27.00) + 29.90 + \
            (27.00) + 25.90 + (29.00) + 58.40 + (29.00) + 58.40 + (29.00) + 58.40 + 29.00 + \
            39.90 + 58.40 + 69.90 + 44.00 + 69.90 + 58.40 + 62.90 + 44.00 + \
            v_card + (18 * vie_day)
    x2018 = 19.90 + 43.90 + 39.00 + 44.00 + 31.15 + 149.80 + 34.40 + 44.40 + 58.60 + 48.15 + \
            79.90 + 44.90 + 48.00 + 35.50 + 55.60 + 42.00 + 12.90 + 37.40 + 60.40 + 29.90 + \
            44.00 + 42.00 + 42.00 + 89.80 + 43.50 + v_card + (14 * vie_day)
    x2019 = 44.00 + 16.10 + 41.80 + 59.90 + 44.00 + 29.00 + 31.85 + 27.80 + 43.65 + 44.00 + \
            39.90 + 16.40 + 27.80 + 14.90 + 27.80 + 19.40 + 27.80 + 59.90 + 67.15 + 74.65 + \
            35.15 + 43.65 + 39.90 + 39.90 + 43.15 + 74.65 + 29.00 + 44.00 + 78.05 + 60.15 + \
            39.90 + v_card + (14 * vie_day)

    print(f"2017 cost: {x2017}\n2018 cost: {x2018}\n2019 cost: {x2019}")


# Test all combinations
handle_kwargs("I am all alone")
handle_kwargs("I have a naughty friend", invalid_a=False, invalid_b=None, invalid_c="naughty")
handle_kwargs("I have incompatible style", local_style="this is not good")
handle_kwargs("I have true style", local_style=True)
handle_kwargs("I am template", custom_template="fill me in")
handle_kwargs("I am everything", local_style=True, custom_template="on display")
