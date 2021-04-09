from src.make_a_comment.adapters.controllers.cli.commands.user.register_user import register_user


def register_register_user_parser(subparsers):
    parser = subparsers.add_parser(
        "register_user", help="use to register user in database")

    parser.set_defaults(func=register_user)

    parser.add_argument(
        "name", type=str, help="user name", metavar="name")
    parser.add_argument(
        "email", type=str, help="user email", metavar="email")
    parser.add_argument(
        "password", type=str, help="user password", metavar="password")
