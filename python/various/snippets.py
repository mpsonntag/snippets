import hashlib

print(hashlib.sha1(b"abcdefg@cd").hexdigest())


# kwargs example
def conditional_print(filename, local_style=True, custom_template=None):
    print("filename: %s, local_style: %s, custom_template: %s" % (filename, local_style,
                                                                  custom_template))


def handle_kwargs(filename, **kwargs):
    local_style = False
    custom_template = None

    if "local_style" in kwargs and isinstance(kwargs["local_style"], bool):
        local_style = kwargs["local_style"]
    if "custom_template" in kwargs and isinstance(kwargs["custom_template"], str):
        custom_template = kwargs["custom_template"]
    conditional_print(filename, local_style, custom_template)


def scale_print(add_trips=0):
    curr = 1440 + 120+60
    pot = 949 + 600
    if not add_trips:
        print(f"Current: {curr}\tklimaticket: {pot}")
    for i in range(add_trips):
        curr_add = i * (120 + 10)
        pot_add = i * 50
        print(f"Current: {curr + curr_add}\tklimaticket: {pot + pot_add}\tadd trip {i}")


# Test all combinations
handle_kwargs("I am all alone")
handle_kwargs("I have a naughty friend", invalid_a=False, invalid_b=None, invalid_c="naughty")
handle_kwargs("I have incompatible style", local_style="this is not good")
handle_kwargs("I have true style", local_style=True)
handle_kwargs("I am template", custom_template="fill me in")
handle_kwargs("I am everything", local_style=True, custom_template="on display")
