# import argparse

# https://stackoverflow.com/questions/43075087/format-argparse-help-for-positional-arguments
# def print_help(parser):
#     help_message = ""
#     help_message += str(parser.description)
#     help_message += "\ncommands:\n"

#     subparsers_actions = [
#         action for action in parser._actions
#         if isinstance(action, argparse._SubParsersAction)]

#     for subparsers_action in subparsers_actions:
#         for choice in subparsers_action._choices_actions:
#             help_message += "\n"
#             help_message += "    {:<30} {}".format(choice.dest, choice.help)

#     print(help_message)
