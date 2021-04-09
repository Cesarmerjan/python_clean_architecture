from src.make_a_comment.adapters.controllers.cli.commands.user.login import login


def register_login_parser(subparsers):
    parser = subparsers.add_parser(
        "login", help="make login")

    parser.set_defaults(func=login)

    parser.add_argument(
        "email", type=str, help="user email", metavar="email")

    parser.add_argument(
        "password", type=str, help="user password", metavar="password")
