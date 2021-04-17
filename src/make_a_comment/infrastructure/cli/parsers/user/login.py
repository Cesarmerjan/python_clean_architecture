from src.make_a_comment.adapters.controllers.cli.commands.user.login import login


def register_login_parser(subparsers):
    parser = subparsers.add_parser(
        "login", help="Use to make login",
        description="You can use this command to login. You will receve an access_token",
        usage="")

    parser.set_defaults(func=login)

    parser.add_argument(
        "email", type=str, help="user email", metavar="email")

    parser.add_argument(
        "password", type=str, help="user password", metavar="password")
