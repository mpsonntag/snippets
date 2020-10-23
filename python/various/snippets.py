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


# Test all combinations
handle_kwargs("I am all alone")
handle_kwargs("I have a naughty friend", invalid_a=False, invalid_b=None, invalid_c="naughty")
handle_kwargs("I have incompatible style", local_style="this is not good")
handle_kwargs("I have true style", local_style=True)
handle_kwargs("I am template", custom_template="fill me in")
handle_kwargs("I am everything", local_style=True, custom_template="on display")
