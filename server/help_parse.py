file = open("help_msg.txt", "r")


def help_msg():
    help = ""
    for line in file:
        help += line
    return help
